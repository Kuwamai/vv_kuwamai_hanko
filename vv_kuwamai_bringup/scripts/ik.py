#!/usr/bin/env python
# coding: utf-8

import rospy
import geometry_msgs.msg
from sensor_msgs.msg import JointState
import numpy as np

class Arm_ik:
    def __init__(self):
        self._sub_pos = rospy.Subscriber("/arm_pos", geometry_msgs.msg.Point, self.pos_callback)
        self.pub = rospy.Publisher("vv_kuwamai/master_joint_state", JointState, queue_size=10)
        
        #初期位置
        self.pos = geometry_msgs.msg.Point()
        self.pos.x = 0.1
        self.pos.z = 0.1

        self.r = rospy.Rate(20)

        #最大関節角速度
        self.max_vel = 0.3

        #初期角度
        self.q = self.q_old = np.array([[0],
                                        [0],
                                        [np.pi/2]])

    def pos_callback(self, message):
        self.pos = message

    #逆運動学計算
    def ik(self):
        while not rospy.is_shutdown():
            #目標手先位置
            r_ref = np.array([[self.pos.x],
                              [self.pos.y],
                              [self.pos.z]])

            #特異姿勢回避
            r_ref = self.singularity_avoidance(r_ref)

            r = self.fk(self.q)
            if np.linalg.norm(r - r_ref, ord=2) > 0.0001:
                #数値計算
                for i in range(10):
                    r = self.fk(self.q)
                    if np.linalg.norm(r - r_ref, ord=2) < 0.0001:
                        break
                    self.q = self.q - np.linalg.inv(self.J(self.q)).dot((r - r_ref))

                self.angular_vel_limit()

                js = JointState()
                js.name=["joint_{}".format(i) for i in range(3)]
                js.position = [self.q[0,0], self.q[1,0], self.q[2,0]]
                self.pub.publish(js)
                self.r.sleep()

    #同次変換行列
    def trans_m(self, a, alpha, d, theta):
        m = np.array([[np.cos(theta), -np.sin(theta), 0., a],
                      [np.cos(alpha)*np.sin(theta), np.cos(alpha)*np.cos(theta), -np.sin(alpha), -np.sin(alpha)*d],
                      [np.sin(alpha)*np.sin(theta), np.sin(alpha)*np.cos(theta),  np.cos(alpha),  np.cos(alpha)*d],
                      [0., 0., 0., 1.]])
        return m

    #順運動学
    def fk(self, theta):
        tm0_1 = self.trans_m(0,   0,       0, theta[0,0]+np.pi)
        tm1_2 = self.trans_m(0,   np.pi/2, 0, theta[1,0]+np.pi/2)
        tm2_3 = self.trans_m(0.1, 0,       0, theta[2,0])
        tm3_4 = self.trans_m(0.1, 0,       0, 0)
        pos = tm0_1.dot(tm1_2).dot(tm2_3).dot(tm3_4)[0:3,3:4]
        return pos

    #ヤコビ行列
    def J(self, theta):
        e = 1.0e-10
        diff_q1 = (self.fk(theta+np.array([[e],[0.],[0.]]))-self.fk(theta))/e
        diff_q2 = (self.fk(theta+np.array([[0.],[e],[0.]]))-self.fk(theta))/e
        diff_q3 = (self.fk(theta+np.array([[0.],[0.],[e]]))-self.fk(theta))/e
        return np.hstack((diff_q1, diff_q2, diff_q3))

    #角速度制限
    def angular_vel_limit(self):
        q_diff = self.q - self.q_old
        q_diff_max = np.abs(q_diff).max()

        if(q_diff_max > self.max_vel):
            rospy.loginfo("Too fast")
            q_diff /= q_diff_max
            q_diff *= self.max_vel
            self.q = self.q_old + q_diff

        self.q_old = self.q

    #特異姿勢回避
    def singularity_avoidance(self, r_ref):
        #コントローラ位置がアームの可動範囲を超えた際はスケール
        r_ref_norm = np.linalg.norm(r_ref, ord=2)

        if r_ref_norm > 0.19:
            rospy.loginfo("Out of movable range")
            r_ref /= r_ref_norm
            r_ref *= 0.19

        #目標位置がz軸上付近にある際はどける
        r_ref_xy_norm = np.linalg.norm(r_ref[0:2], ord=2)

        if r_ref_xy_norm < 0.01:
            rospy.loginfo("Avoid singular configuration")
            r_ref[0] = 0.01

        return r_ref

if __name__ == '__main__':
    try:
        rospy.init_node('arm_ik')
        arm_ik = Arm_ik()
        arm_ik.ik()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
