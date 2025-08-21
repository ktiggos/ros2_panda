cmake_minimum_required(VERSION 3.8)
project(panda_moveit)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_visual_tools REQUIRED)
find_package(control_msgs)

add_executable(panda_cartesian_planning src/panda_cartesian_planning.cpp)
add_executable(path_publisher src/path_publisher.cpp)

target_include_directories(panda_cartesian_planning
  PUBLIC include
)

ament_target_dependencies(panda_cartesian_planning 
  rclcpp
  control_msgs
  geometry_msgs
  moveit_msgs
  moveit_ros_planning_interface
  moveit_visual_tools
)

ament_target_dependencies(path_publisher
  rclcpp
  geometry_msgs
  nav_msgs
)

install(TARGETS
  panda_cartesian_planning
  path_publisher
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

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

ament_package()