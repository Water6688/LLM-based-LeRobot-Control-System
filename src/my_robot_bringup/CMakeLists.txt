cmake_minimum_required(VERSION 3.8)
project(my_robot_bringup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)


install(
  DIRECTORY config launch worlds
  DESTINATION share/${PROJECT_NAME}/
)
install(
  PROGRAMS
  scripts/arm_control_test.py
  scripts/angle_sync_test.py
  scripts/joint_state_monitor.py
  scripts/joint_state_test.py
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
