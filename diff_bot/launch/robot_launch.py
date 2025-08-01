from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessStart
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
import os
import xacro

pkg_name = "diff_bot"

# Function to include the rsp.launch.py file
def include_rsp_launch():
    rsp_file = "rsp.launch.py"
    rsp_path = os.path.join(FindPackageShare(pkg_name).find(pkg_name), "launch", rsp_file)
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_path])
    )

# Function to load and process the xacro file
def load_and_process_xacro():
    urdf_file_name = "robot.urdf.xacro"
    urdf_path = os.path.join(FindPackageShare(pkg_name).find(pkg_name), "urdf", urdf_file_name)
    robot_desc = xacro.process_file(urdf_path)
    return robot_desc.toxml()

# Function to create the ros2_control node
def create_controller_manager_node(xacro_description):
    controller_params_file = os.path.join(FindPackageShare(pkg_name).find(pkg_name), 'config', 'diff_drive_controller.yaml')


    return Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{"robot_description": xacro_description}, controller_params_file]
    )

# Function to create the controller spawner node
def create_controller_spawner_node(controller_name):
    return Node(
        package="controller_manager",
        executable="spawner",
        arguments=[controller_name]
    )

# Function to create the delayed controller spawner
def create_delayed_controller_spawner(controller_manager_node, spawner_node):
    return RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager_node,
            on_start=[spawner_node],
        )
    )
# Main launch file generation
def generate_launch_description():
    rsp_launch = include_rsp_launch()
    xacro_description = load_and_process_xacro()

    controller_manager_node = create_controller_manager_node(xacro_description)
    diff_drive_spawner_node = create_controller_spawner_node("diff_cont")
    joint_broad_spawner_node = create_controller_spawner_node("joint_broad")

    delayed_diff_drive_spawner = create_delayed_controller_spawner(controller_manager_node, diff_drive_spawner_node)
    delayed_joint_broad_spawner = create_delayed_controller_spawner(controller_manager_node, joint_broad_spawner_node)
    
    lidar = Node(
    package='rplidar_ros',
    executable='rplidar_composition',
    output='screen',
    parameters=[{
        'serial_port': '/dev/ttyUSB0',
        'serial_baudrate': 115200,   # A1 / A2
        # 'serial_baudrate': 256000, # A3
        'frame_id': 'laser_frame',
        'inverted': False,
        'angle_compensate': True,
    }])
    cmd_vel_mapper = Node(
        package="diff_bot",
        executable="cmd_vel_mapper",
        output="screen"
    )
    return LaunchDescription([
        rsp_launch,
        TimerAction(period=3.0, actions=[controller_manager_node]),  # Delayed start of the controller manager
        delayed_diff_drive_spawner,  # Delayed start of the diff drive spawner
        delayed_joint_broad_spawner,  # Delayed start of the joint broad spawner
        lidar,
        cmd_vel_mapper
    ])