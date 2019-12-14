cmake_minimum_required(VERSION 2.8.3)
project(vv_kuwamai_apps)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  genmsg
  actionlib_msgs
)

add_action_files(
  FILES
  HankoWp.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  geometry_msgs
)

catkin_package(
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
