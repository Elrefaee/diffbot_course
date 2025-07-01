import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'diff_bot'

    # === Paths ===
    pkg_diffbot = get_package_share_directory(pkg_name)
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    rsp_path = os.path.join(pkg_diffbot, 'launch', 'rsp.launch.py')
    gazebo_launch_path = os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
    world_path = os.path.join(pkg_diffbot, 'worlds', 'sim_world.world')
    rviz_config_path = os.path.join(pkg_diffbot, 'rviz', 'show_robot.rviz')

    # === Launch Configuration
    use_rviz = LaunchConfiguration('rviz', default='false')

    # === Launch robot_state_publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_path)
    )

    # === Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path),
        launch_arguments={'world': world_path}.items()
    )

    # === Spawn robot in Gazebo
    spawn_entity = TimerAction(  # slight delay to allow gazebo to initialize
        period=2.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name='spawn_entity',
                arguments=[
                    '-topic', 'robot_description',
                    '-entity', 'my_bot'
                ],
                output='screen'
            )
        ]
    )

    # === Optional RViz launch
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        condition=IfCondition(use_rviz),
        output='screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        rviz
    ])
