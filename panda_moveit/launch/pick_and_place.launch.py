#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

WB_PKG = 'panda_webots'
MOVE_PKG = "panda_moveit"

def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def generate_launch_description():
    webots_pkg = get_package_share_directory(WB_PKG)
    moveit_pkg = get_package_share_directory(MOVE_PKG)

    urdf_path = os.path.join(webots_pkg, 'description', 'panda', 'panda.urdf')
    srdf_path = os.path.join(moveit_pkg, "config", "panda.srdf")
    kin_yaml  = os.path.join(moveit_pkg, "config", "yaml", "kinematics.yaml")

    pick_and_place = Node(
        name="panda_pick_and_place",
        package="panda_moveit",
        executable="panda_pick_and_place",
        output="screen",
        parameters=[
            {"robot_description": read_file(urdf_path)},
            {"robot_description_semantic": read_file(srdf_path)},
            kin_yaml,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([pick_and_place])