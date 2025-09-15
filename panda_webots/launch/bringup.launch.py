import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

PKG_NAME = 'panda_webots'

def generate_launch_description():

    ### Parameters ###
    # All parameters need to be type STR
    gui = "true"
    world = "empty_world.wbt"
    ##################

    pkg_dir = get_package_share_directory(PKG_NAME)

    launch_dir = os.path.join(pkg_dir,"launch/")

    webots = IncludeLaunchDescription(
        os.path.join(launch_dir,"webots.launch.py"),
        launch_arguments={'gui': gui, 'world': world}.items()
    )

    robot_nodes = IncludeLaunchDescription(
        os.path.join(launch_dir, "robot_nodes.launch.py")
    )

    return LaunchDescription([
        webots,
        robot_nodes
    ])