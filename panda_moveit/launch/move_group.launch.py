#!/usr/bin/env python3
import os
import pathlib
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

WB_PKG = 'panda_webots'
MOVE_PKG = 'panda_moveit'

def read_file(path):
    with open(path, 'r') as f:
        return f.read()
    
def generate_launch_description():
    webots_pkg = get_package_share_directory(WB_PKG)
    moveit_pkg = get_package_share_directory(MOVE_PKG)

    # Paths
    urdf_path = os.path.join(webots_pkg, 'description', 'panda', 'panda.urdf')
    srdf_path = os.path.join(moveit_pkg, 'config', 'panda.srdf')
    kin_yaml = os.path.join(moveit_pkg, 'config/yaml', 'kinematics.yaml')
    # ctrl_yaml = os.path.join(moveit_pkg, 'config/yaml', 'controllers.yaml')
    ompl_yaml = os.path.join(moveit_pkg, 'config/yaml', 'ompl_planning_minimal.yaml')

    # Params
    robot_description = read_file(urdf_path)
    robot_description_semantic = read_file(srdf_path)

    move_group_params = [
        {'robot_description': robot_description},
        {'robot_description_semantic': robot_description_semantic},
        kin_yaml,
        # ctrl_yaml,
        # Use control interface for automatic controller discovery
        {'moveit_controller_manager': 'moveit_ros_control_interface/Ros2ControlManager'},
        ompl_yaml,
        {'use_sim_time': True},
        {'planning_scene_monitor.publish_planning_scene': True},
        {'planning_scene_monitor.publish_geometry_updates': True},
        {'planning_scene_monitor.publish_state_updates': True},
        {'planning_scene_monitor.publish_transforms_updates': True},
        {'allow_trajectory_execution': True},
    ]

    move_group = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=move_group_params,
    )

    return LaunchDescription([move_group])
