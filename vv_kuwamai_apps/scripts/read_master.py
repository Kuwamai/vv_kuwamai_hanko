#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------------------
#Name : read_master.py
#Author : s-shibata
#Created : 2019 / 10 / 01
#Last Date : 2019 / 11 / 25
#Note : Related to vsearch.py and gene_image.py
#---------------------------------------------------

import shutil
from distutils.dir_util import copy_tree
import os
import vsearch
import glob
import cv2
import vv_print

import rospy
import actionlib
import geometry_msgs.msg
from vv_kuwamai_apps.msg import *
from std_srvs.srv import Empty

import time

def send_position():
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

def send_snapshot_position():
    goal = HankoWpGoal()
    goal.hanko_pos.x = 0.06
    goal.hanko_pos.y = 0.0
    goal.hanko_pos.z = 0.16
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(30.0))

def call_service():
    rospy.loginfo('waiting service')
    rospy.wait_for_service('call_me')
    try:
        service = rospy.ServiceProxy('call_me', Empty)
        response = service()
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

if __name__ == '__main__':
    rospy.init_node("wp_client")
    client = actionlib.SimpleActionClient("gen_wp", HankoWpAction)
    client.wait_for_server()
    while(1):
        if True:
            print "start vsearch"
            ma = vsearch.Search()
            ma.kuwamai()
            vp = vv_print.VVPrint()
            L = glob.glob('/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data/*')
            print "len L"
            print len(L)
            for i in range(len(L)):
                print "print and upload"
                filename = L[i]
                print filename
                vp.test_print(filename)

                # send goal position
                send_position()

                time.sleep(2.0)

                # upload to twitter
                send_snapshot_position()
                call_service()

                copy_tree("/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data", "/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data1")
                target_dir = "/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data"
                shutil.rmtree(target_dir)
                os.mkdir(target_dir)

        else:
            break
            print "exit"

        rospy.loginfo('start sleep') 
        time.sleep(10.0)
        rospy.loginfo('end sleep') 
