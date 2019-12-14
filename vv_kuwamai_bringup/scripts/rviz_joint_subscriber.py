#!/usr/bin/env python
# coding: utf-8

import rospy
import math
from sensor_msgs.msg import JointState

class RvizSlave:
    def __init__(self):
        self.sub = rospy.Subscriber("/vv_kuwamai/master_joint_state", JointState, self.joint_callback, queue_size=10)
        self.pub = rospy.Publisher("joint_states_source", JointState, queue_size=10)
        self.r = rospy.Rate(30)

    def joint_callback(self, msg):
        js = JointState()

        for i in range(3):
            js.name.append("joint_"+str(i))
            js.position.append(msg.position[i])

        self.pub.publish(js)
        self.r.sleep()

if __name__ == "__main__":
    try:
        while not rospy.is_shutdown():
            rospy.init_node("rviz_joint_state_subscriber")
            rviz = RvizSlave()
            rospy.spin()

    except rospy.ROSInterruptException:
        pass
