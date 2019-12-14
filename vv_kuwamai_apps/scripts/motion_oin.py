#! /usr/bin/env python

import rospy
import actionlib
import geometry_msgs.msg
from vv_kuwamai_apps.msg import *

if __name__ == '__main__':
    rospy.init_node("wp_client")
    client = actionlib.SimpleActionClient("gen_wp", HankoWpAction)
    client.wait_for_server()

    rospy.loginfo("syuniku no ue")
    goal = HankoWpGoal()
    goal.hanko_pos.x = 0.0
    goal.hanko_pos.y = 0.075
    goal.hanko_pos.z = 0.05
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("syuniku osu")
    goal.hanko_pos.z = -0.01
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("syuniku no ue")
    goal.hanko_pos.z = 0.05
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("oin no ue")
    goal.hanko_pos.x = 0.125
    goal.hanko_pos.y = 0.01
    goal.hanko_pos.z = 0.03
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("oin")
    goal.hanko_pos.x = 0.11
    goal.hanko_pos.z = 0.0
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    goal.hanko_pos.x = 0.095
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    goal.hanko_pos.x = 0.11
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("oin no ue")
    goal.hanko_pos.x = 0.125
    goal.hanko_pos.z = 0.05
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

    rospy.loginfo("Done")
    goal.hanko_pos.x = 0.1
    goal.hanko_pos.y = 0.0
    goal.hanko_pos.z = 0.1
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))
