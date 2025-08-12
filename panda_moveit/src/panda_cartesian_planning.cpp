#include <vector>
#include <cmath>
#include <chrono>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/path.hpp>

#include <moveit_msgs/msg/robot_trajectory.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_visual_tools/moveit_visual_tools.h>

static const rclcpp::Logger LOGGER{rclcpp::get_logger("PCP")};

nav_msgs::msg::Path TARGET_PATH;
bool GOT_PATH{false};

void callback(const nav_msgs::msg::Path& path_msg){
    TARGET_PATH = path_msg;
    GOT_PATH = true;
}

int main(int argc, char* argv[])
{
    rclcpp::init(argc,argv);

    rclcpp::NodeOptions node_opts;

    node_opts.automatically_declare_parameters_from_overrides(true);
    auto node = rclcpp::Node::make_shared("panda_cartesian_planning", node_opts);

    // // Spin executor on a single thread
    // rclcpp::executors::SingleThreadedExecutor executor;
    // executor.add_node(node);

    // std::thread([&executor](){executor.spin();}).detach();

    // Setup planning interface
    static const std::string PLANNING_GROUP{"panda_arm"};
    moveit::planning_interface::MoveGroupInterface move_group(node, PLANNING_GROUP);

    // Get path
    auto sub = node->create_subscription<nav_msgs::msg::Path>("target_path",10, callback);
    while(rclcpp::ok()){

        rclcpp::spin_some(node);

        if(GOT_PATH){break;};
    }

    RCLCPP_INFO(LOGGER, "PATH SIZE: %li pts", TARGET_PATH.poses.size());

    // Path to Pose Vector
    geometry_msgs::msg::Pose start_pose, setup_pose, point;
    std::vector<geometry_msgs::msg::Pose> waypoints;

    double effz_bias = 0.058*1.75; // End-effector position bias (z-axis)

    // Starting position
    start_pose.position.x = 0.307;
    start_pose.position.y = 0.0;
    start_pose.position.z = 0.590;

    start_pose.orientation.x = 1.0;
    start_pose.orientation.y = 0.0;
    start_pose.orientation.z = 0.0;
    start_pose.orientation.w = 0.0;

    // Set-up position
    setup_pose.position.x = 0.5;
    setup_pose.position.y = 0.0;
    setup_pose.position.z = 0.6;

    setup_pose.orientation.x = 1.0;
    setup_pose.orientation.y = 0.0;
    setup_pose.orientation.z = 0.0;
    setup_pose.orientation.w = 0.0;

    waypoints.push_back(setup_pose);
    for(geometry_msgs::msg::PoseStamped pose_stamped : TARGET_PATH.poses){
        point.orientation = pose_stamped.pose.orientation;
        point.position = pose_stamped.pose.position;

        // Add end-effector bias to z
        point.position.z += effz_bias;

        waypoints.push_back(point);
    }

    // Stage 1: Start position goal
    move_group.setPoseTarget(setup_pose);
    moveit::planning_interface::MoveGroupInterface::Plan setup_plan;

    bool success = (move_group.plan(setup_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    RCLCPP_INFO(LOGGER, "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");

    move_group.move();

    // Stage 2: Cartesian path planning
    moveit_msgs::msg::RobotTrajectory trajectory;

    const double jump_threshold{0.0};
    const double eef_step{0.01};
    move_group.setStartStateToCurrentState();
    double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

    RCLCPP_INFO(LOGGER,"Cartesian path converted to trajectory (%.2f%% achieved)", fraction*100.0);

    move_group.execute(trajectory);

    // Stage 3: Move to starting position
    move_group.setPoseTarget(start_pose);
    moveit::planning_interface::MoveGroupInterface::Plan recovery_plan;

    success = (move_group.plan(recovery_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    RCLCPP_INFO(LOGGER, "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");

    move_group.move();

    return 0;
}