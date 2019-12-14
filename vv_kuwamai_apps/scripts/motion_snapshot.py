#! /usr/bin/env python

import rospy
import actionlib
import geometry_msgs.msg
from vv_kuwamai_apps.msg import *

if __name__ == '__main__':
    rospy.init_node("wp_client")
    client = actionlib.SimpleActionClient("gen_wp", HankoWpAction)
    client.wait_for_server()

    goal = HankoWpGoal()
    goal.hanko_pos.x = 0.15
    goal.hanko_pos.y = 0.0
    goal.hanko_pos.z = 0.1
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("Say cheese!")

    goal.hanko_pos.x = 0.1
    goal.hanko_pos.y = 0.0
    goal.hanko_pos.z = 0.1
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("Done")
