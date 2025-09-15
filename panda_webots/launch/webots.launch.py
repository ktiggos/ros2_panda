import launch
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from webots_ros2_driver.webots_launcher import WebotsLauncher

PKG_NAME = 'panda_webots'

def _launch_setup(conext, *args, **kwargs):
    pkg_dir = get_package_share_directory(PKG_NAME)
    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')

    gui_str = gui.perform(conext)

    # Check gui arg validity
    if not (gui_str.lower() == 'true' or gui_str.lower() == 'false'):
        raise TypeError(f"Expected gui argument value 'true' or 'false' but got {gui_str}")
    else:
        # Get boolean based on launch argument 'gui'
        gui_bool = gui_str.lower() == 'true'

    webots = WebotsLauncher(
        world=PathJoinSubstitution([pkg_dir,'worlds',world]),
        gui=gui_bool,
        ros2_supervisor=True,
        output='screen'
    )

    return [
        webots,
        webots._supervisor,
        launch.actions.RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())]
            )
        )
    ]


def generate_launch_description():

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='empty_world.wbt'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='True'
        ),
        OpaqueFunction(function=_launch_setup)
    ])