cmake_minimum_required(VERSION 3.5)
project(r1)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# Install the Python script
install(PROGRAMS
  src/robot_movement.py
  src/camera_node.py
  src/odometry.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install other directories
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

