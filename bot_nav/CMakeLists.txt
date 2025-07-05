cmake_minimum_required(VERSION 3.8)
project(bot_nav)

# Enable strict compiler warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Required dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

# Install all non-code resources
install(
  DIRECTORY
    launch
    config
    maps
    rviz
  DESTINATION
    share/${PROJECT_NAME}
)

# Optional: Install source nodes
# add_executable(my_node src/my_node.cpp)
# ament_target_dependencies(my_node rclcpp)
# install(TARGETS my_node DESTINATION lib/${PROJECT_NAME})

# Enable linting
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# Export the package
ament_package()
