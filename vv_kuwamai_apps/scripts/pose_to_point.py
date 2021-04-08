#!/usr/bin/env python
# coding: utf-8

import rospy
import geometry_msgs.msg

def pose_callback(message):
    point_pub.publish(message.position)

pose_sub = rospy.Subscriber("/arm_pose", geometry_msgs.msg.Pose, pose_callback)
point_pub = rospy.Publisher("/arm_pos", geometry_msgs.msg.Point, queue_size=1)

if __name__ == "__main__":
    rospy.init_node('pose_to_point')
    rospy.spin()
