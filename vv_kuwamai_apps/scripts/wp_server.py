#!/usr/bin/env python
# coding: utf-8

import rospy
import geometry_msgs.msg
import actionlib
from vv_kuwamai_apps.msg import *
import numpy as np

class HankoWpServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer("gen_wp", HankoWpAction, self.execute, False)
        self.server.start()

        self.pub = rospy.Publisher("arm_pos", geometry_msgs.msg.Point, queue_size=10)

        self.home_pos = geometry_msgs.msg.Point()
        self.home_pos.x = 0.1
        self.home_pos.y = 0.0
        self.home_pos.z = 0.1

        self.r = rospy.Rate(20)

    def execute(self, goal):
        goal_pos = goal.hanko_pos

        x_mov = np.linspace(self.home_pos.x, goal_pos.x, 50)
        y_mov = np.linspace(self.home_pos.y, goal_pos.y, 50)
        z_mov = np.linspace(self.home_pos.z, goal_pos.z, 50)

        pub_pos = geometry_msgs.msg.Point()

        for x, y, z in zip(x_mov, y_mov, z_mov):
            pub_pos.x = x
            pub_pos.y = y
            pub_pos.z = z
            self.pub.publish(pub_pos)
            self.r.sleep()

        self.home_pos = goal_pos
        self.server.set_succeeded()

if __name__ == '__main__':
    rospy.init_node('wp_server')
    server = HankoWpServer()
    rospy.spin()
