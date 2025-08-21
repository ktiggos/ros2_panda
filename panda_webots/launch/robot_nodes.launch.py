import os
import launch
from launch.event_handlers import OnProcessIO
from launch.event_handlers import OnProcessExit
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.urdf_spawner import URDFSpawner, get_webots_driver_node
from webots_ros2_driver.webots_controller import WebotsController

PKG_NAME = 'panda_webots'

def generate_launch_description():
    pkg_dir = get_package_share_directory(PKG_NAME)
    robot_description_path = os.path.join(pkg_dir,'description/panda','panda.urdf')
    ros2_control_config = os.path.join(pkg_dir,'config','ros2_control.yaml')

    controller_manager_timeout = ['--controller-manager-timeout', '100']

    with open(robot_description_path, 'r') as infp:
        lines = infp.readlines()
        robot_description = ''.join(line for line in lines if not line.strip().startswith('<?xml'))

    # Webots Configuration
    spawn_panda = URDFSpawner(
        name='panda',
        urdf_path=robot_description_path,
    )

    panda_driver = WebotsController(
        robot_name='panda',
        parameters=[
            {'robot_description' : robot_description},
            {'use_sim_time' : True},
            {'set_robot_state_publisher' : False},
            ros2_control_config
        ]
    )

    # Node Launching
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description' : robot_description
        }]
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['joint_state_broadcaster', '-c', 'controller_manager'] + controller_manager_timeout
    )

    panda_arm_controller=Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['panda_arm_controller', '-c', 'controller_manager']+controller_manager_timeout
    )

    startup_pose_node = Node(
        package='panda_webots',
        executable='panda_startup_pose.py',
        output='screen'
    )

    return LaunchDescription([
        spawn_panda,
        robot_state_publisher,
        joint_state_broadcaster,
        panda_arm_controller,

        # Launch controller manager node after URDF spawn
        launch.actions.RegisterEventHandler(
            event_handler=OnProcessIO(
                target_action=spawn_panda,
                on_stdout= lambda event: get_webots_driver_node(event, panda_driver)
            )
        ),

        # Launch startup pose node after panda controller
        launch.actions.RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=panda_arm_controller,
                on_start=[startup_pose_node]
            )
        ),

        # On driver exit --> killall
        launch.actions.RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=panda_driver,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())]
            )
        )
    ])