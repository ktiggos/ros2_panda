import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

WB = 'panda_webots'
RVIZ = 'panda_viz'

def generate_launch_description():

    ### Parameters ###
    # All parameters need to be type STR
    gui = "true"
    world = "milling_world.wbt"
    ##################

    webots_pkg = get_package_share_directory(WB)
    rviz_pkg = get_package_share_directory(RVIZ)

    launch_dir = os.path.join(webots_pkg,"launch/")

    webots = IncludeLaunchDescription(
        os.path.join(os.path.join(webots_pkg,"launch/"),"webots.launch.py"),
        launch_arguments={'gui': gui, 'world': world}.items()
    )

    robot_nodes = IncludeLaunchDescription(
        os.path.join(launch_dir, "robot_nodes.launch.py")
    )

    rviz = IncludeLaunchDescription(
        os.path.join(os.path.join(rviz_pkg,"launch/"),"panda_viz.launch.py")
    )

    return LaunchDescription([
        webots,
        robot_nodes,
        rviz,
    ])