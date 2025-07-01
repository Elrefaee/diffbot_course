import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    # === Paths ===
    pkg_diffbot = get_package_share_directory('diff_bot')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    rsp_path = os.path.join(pkg_diffbot, 'launch', 'rsp.launch.py')
    gazebo_launch_path = os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')

    # === Include robot_state_publisher launch ===
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_path)
    )

    # === Include Gazebo simulation environment ===
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path)
    )

    # === Spawn robot into Gazebo ===
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_bot'
        ],
        output='screen'
    )

    # === Final Launch Description ===
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])
