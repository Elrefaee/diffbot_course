cmake_minimum_required(VERSION 3.8)
project(diff_bot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_executable(cmd_vel_mapper src/cmd_vel_mapper.cpp)

ament_target_dependencies(cmd_vel_mapper
  rclcpp
  geometry_msgs
)

install(TARGETS
  cmd_vel_mapper
  DESTINATION lib/${PROJECT_NAME}
)


install(
  DIRECTORY
  urdf
  launch
  config
  worlds
  rviz
  src
  DESTINATION
  share/${PROJECT_NAME}
)

ament_package()
