from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("moveit_resources_panda").to_moveit_configs()

    # MoveGroupInterface demo executable
    move_group_demo = Node(
        name="panda_cartesian_planning",
        package="panda_moveit",
        executable="panda_cartesian_planning",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
    )

    path_publisher = Node(
        name="path_publisher",
        package="panda_moveit",
        executable="path_publisher",
        output="screen",
        parameters=[
            {'circle_center_x' : '0.5'}
        ]
    )

    return LaunchDescription([
        path_publisher,
        move_group_demo,
    ])