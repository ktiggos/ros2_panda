from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    gui_arg = DeclareLaunchArgument('gui', default_value='false',
                                    description='Set to "false" to launch Gazebo without GUI')
    
    gui = LaunchConfiguration('gui')

    # Path to URDF
    pkg_share = get_package_share_directory('panda_gazebo')
    urdf_path = os.path.join(pkg_share, 'description', 'panda', 'panda.urdf')

    # Read URDF file
    with open(urdf_path, 'r') as infp:
        lines = infp.readlines()
        robot_description = ''.join(line for line in lines if not line.strip().startswith('<?xml'))


    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'gui': gui}.items()
    )

    jsp_node = Node(package='joint_state_publisher',
                    executable='joint_state_publisher',
                    name='joint_state_publisher',
                    output='screen')
    
    rsp_node = Node(package='robot_state_publisher',
                    executable='robot_state_publisher',
                    name='robot_state_publisher',
                    parameters=[{'robot_description': robot_description,
                                 'use_sim_time': True}],
                    output='screen')

    spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'panda',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0'],
        output='screen'
    )

    return LaunchDescription([
        gui_arg,
        gazebo_launch,
        jsp_node,
        rsp_node,
        spawn_node
    ])