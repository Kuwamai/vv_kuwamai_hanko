cmake_minimum_required(VERSION 2.8.3)
project(vv_kuwamai_bringup)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_library(rs30x STATIC src/rs30x.cpp)
add_executable(joint_subscriber src/joint_subscriber.cpp)
target_link_libraries(joint_subscriber rs30x)
target_link_libraries(joint_subscriber ${catkin_LIBRARIES})
