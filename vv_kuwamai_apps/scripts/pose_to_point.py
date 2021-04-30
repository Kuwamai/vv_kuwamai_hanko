#!/usr/bin/env python
# coding: utf-8

import rospy
import geometry_msgs.msg
import numpy as np

class PoseToPoint:
    def __init__(self):
        rospy.init_node('pose_to_point')
        self.pose_sub = rospy.Subscriber("/arm_pose", geometry_msgs.msg.Pose, self.pose_callback)
        self.point_pub = rospy.Publisher("/arm_pos", geometry_msgs.msg.Point, queue_size=1)
        self.pose_msg = rospy.wait_for_message("/arm_pose", geometry_msgs.msg.Pose)

        self.x_max = rospy.get_param("/pose_to_point/x_max")
        self.x_min = rospy.get_param("/pose_to_point/x_min")
        self.y_max = rospy.get_param("/pose_to_point/y_max")
        self.y_min = rospy.get_param("/pose_to_point/y_min")
        self.z_max = rospy.get_param("/pose_to_point/z_max")
        self.z_min = rospy.get_param("/pose_to_point/z_min")
        self.pos_scale = rospy.get_param("/pose_to_point/pos_scale")

        self.rate = rospy.Rate(30)
 
    def pose_callback(self, msg):
        self.pose_msg = msg

    def convert(self):
        while not rospy.is_shutdown():
            pos = np.array([self.pose_msg.position.x, self.pose_msg.position.y, self.pose_msg.position.z])
            pos = pos * self.pos_scale
            pos[0] = np.clip(pos[0], self.x_min, self.x_max)
            pos[1] = np.clip(pos[1], self.y_min, self.y_max)
            pos[2] = np.clip(pos[2], self.z_min, self.z_max)

            pos_msg = geometry_msgs.msg.Point()
            pos_msg.x = pos[0]
            pos_msg.y = pos[1]
            pos_msg.z = pos[2]
            self.point_pub.publish(pos_msg)
            self.rate.sleep()
 
if __name__ == '__main__':
    try:
        pose_to_point = PoseToPoint()
        pose_to_point.convert()
        rospy.spin()
    except rospy.ROSInterruptException: pass
