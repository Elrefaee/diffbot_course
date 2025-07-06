#!/bin/bash

# Function to handle user input
handle_input() {
  echo "Enter your command (save / save_inplace): "
  read input

  if [[ "$input" == "save" ]]; then
    ros2 run nav2_map_server map_saver_cli -f my_map
    kill_xterm_and_exit

  elif [[ "$input" == "save_inplace" ]]; then
    cd ~/course_ws/src/bot_nav/maps
    ros2 run nav2_map_server map_saver_cli -f my_map
    cd ~/course_ws
    colcon build --packages-select bot_nav
    kill_xterm_and_exit

  else
    echo "Invalid command. Please enter either 'save' or 'save_inplace'."
  fi
}

# Function to kill the xterm process and exit
kill_xterm_and_exit() {
  killall xterm
  exit
}

# Run the mapping launch file in a new terminal
echo "Running Mapping launch file with RViz"
source /opt/ros/humble/setup.bash
source ~/course_ws/install/setup.bash
xterm -hold -e "ros2 launch bot_nav mapping.launch.py" &

# Continuous prompt for user input
while true; do
  handle_input
done

