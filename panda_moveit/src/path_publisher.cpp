#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <nav_msgs/msg/path.hpp>

#include <vector>
#include <cmath>
static const rclcpp::Logger LOGGER{rclcpp::get_logger("PP")};


std::vector<geometry_msgs::msg::PoseStamped> generate_path(double x0, double y0, double z0, double radius, double dtheta)
{
    std::vector<geometry_msgs::msg::PoseStamped> waypoints;

    double theta{0.0};
    double x{0.0},y{0.0};

    geometry_msgs::msg::PoseStamped point;
    point.header.frame_id = "world";
    point.pose.orientation.x = 1.0;
    point.pose.orientation.y = 0.0;
    point.pose.orientation.z = 0.0;
    point.pose.orientation.w = 0.0;    
    point.pose.position.z = z0; // Circle parallel to XY plane

    RCLCPP_INFO(LOGGER, "Calculating waypoints for circle: x = %0.2f, y = %0.2f, r = %0.2F",x0,y0,radius);

    while(rclcpp::ok()){
        x = x0 + radius*cos(theta);
        y = y0 + radius*sin(theta);

        point.pose.position.x = x;
        point.pose.position.y = y;

        waypoints.push_back(point);

        theta = theta + dtheta;
        if(theta>2*M_PI){break;};
    }

    return waypoints;
}

int main(int argc, char* argv[])
{

    rclcpp::init(argc,argv);
    rclcpp::NodeOptions node_opts;

    node_opts.automatically_declare_parameters_from_overrides(true);
    rclcpp::Node::SharedPtr node = rclcpp::Node::make_shared("path_publisher", node_opts);

    double x0, y0, z0, radius, dtheta;
    std::string path_topic;

    // Load parameters from launch
    node->get_parameter("center_x", x0);
    node->get_parameter("center_y", y0);
    node->get_parameter("center_z", z0);
    node->get_parameter("radius", radius);
    node->get_parameter("dtheta",dtheta);
    node->get_parameter("path_topic",path_topic);

    auto publisher = node->create_publisher<nav_msgs::msg::Path>(path_topic, 10);

    auto waypoints = generate_path(x0, y0, z0, radius, dtheta);

    // Convert vector to Path msg
    nav_msgs::msg::Path target_path;
    target_path.header.frame_id = "world";    
    for(auto wp : waypoints){
        target_path.poses.push_back(wp);
    }

    while(rclcpp::ok()){
        publisher->publish(target_path);
    }

    return 0;
}