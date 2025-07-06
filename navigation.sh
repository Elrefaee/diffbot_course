#!/bin/bash

# Run the Navigation launch file
echo "Running Navigation launch file"
source /opt/ros/humble/setup.bash
source ~/course_ws/install/setup.bash
ros2 launch bot_nav navigation.launch.py
