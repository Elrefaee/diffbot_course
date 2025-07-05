import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition  # <-- مضافة هنا

def generate_launch_description():
    package_name = 'bot_nav'

    map_file = os.path.join(
        get_package_share_directory(package_name),
        'maps',
        'my_map.yaml')

    nav2_yaml = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'amcl_config.yaml')

    rviz_config_file = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        'nav.rviz')

    controller_yaml = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'controller.yaml')

    bt_navigator_yaml = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'bt_navigator.yaml')
    
    planner_yaml = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'planner_server.yaml')



    use_rviz = LaunchConfiguration("rviz", default=True)

    return LaunchDescription([

        # Map Server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'yaml_filename': map_file}
            ]
        ),

        # AMCL
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml]
        ),

        # Controller Server
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml]
        ),

        # Planner Server
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml]
        ),

        # BT Navigator
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[nav2_yaml],
            arguments=['--bt_xml_filename', bt_navigator_yaml]
        ),

        # Lifecycle Manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            parameters=[{'autostart': True},
                        {'node_names': [
                            'map_server',
                            'amcl',
                            'planner_server',
                            'controller_server',
                            'bt_navigator'
                        ]}]
        ),

        # RViz2 (optional)
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_config_file],
            output="screen",
            condition=IfCondition(use_rviz)
        )
    ])
