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

#include <rclcpp_action/rclcpp_action.hpp>
#include <control_msgs/action/follow_joint_trajectory.hpp>
#include <trajectory_msgs/msg/joint_trajectory_point.hpp>

int main(int argc, char* argv[])
{
    rclcpp::init(argc,argv);

    rclcpp::NodeOptions node_opts;

    node_opts.automatically_declare_parameters_from_overrides(true);
    auto node = rclcpp::Node::make_shared("panda_pick_and_place", node_opts);

    // Setup planning interface
    static const std::string PLANNING_GROUP{"panda_arm"};
    moveit::planning_interface::MoveGroupInterface move_group(node, PLANNING_GROUP);

    geometry_msgs::msg::Pose setup_pose;

    setup_pose.position.x = 0.5;
    setup_pose.position.y = 0.0;
    setup_pose.position.z = 0.8;

    setup_pose.orientation.x = 1.0;
    setup_pose.orientation.y = 0.0;
    setup_pose.orientation.z = 0.0;
    setup_pose.orientation.w = 0.0;

    rclcpp::executors::SingleThreadedExecutor exec;
    exec.add_node(node);
    std::thread spinner([&exec](){ exec.spin(); });

    move_group.setPoseTarget(setup_pose);

    moveit::planning_interface::MoveGroupInterface::Plan setup_plan;
    bool success = (move_group.plan(setup_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    if (success) {
    move_group.execute(setup_plan);
    }

    return 0;
}