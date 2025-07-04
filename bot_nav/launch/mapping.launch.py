# File: mapping.launch.py

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_bot_nav = get_package_share_directory('bot_nav')
    config_dir = os.path.join(pkg_bot_nav, 'config')
    slam_config_path = os.path.join(config_dir, 'mapper_params_online_async.yaml')

    slam_toolbox = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='slam_toolbox',
                executable='sync_slam_toolbox_node',
                name='slam_toolbox',
                output='screen',
                parameters=[slam_config_path, {'use_sim_time': True}]
            )
        ]
    )

    map_saver = Node(
        package='nav2_map_server',
        executable='map_saver_server',
        name='map_saver',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_slam',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['slam_toolbox', 'map_saver']
        }]
    )

    return LaunchDescription([
        slam_toolbox,
        map_saver,
        lifecycle_manager
    ])
