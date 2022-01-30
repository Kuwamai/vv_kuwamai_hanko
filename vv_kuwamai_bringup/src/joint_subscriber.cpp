#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include "vv_kuwamai_bringup/rs30x.h"

rs30x servo;
sensor_msgs::JointState armjs;

void joint_callback(const sensor_msgs::JointState msg)
{
    armjs = msg;
}

int main(int argc, char **argv)
{
    const float PI = 3.141592;
    float theta[3] = {0, 0, 90};
    float target[3];
    float offset[3] = {9.5, -3, -10};
    float js_vel = 3;
    float js_ref;
    float js_diff;
    int i;


    for(i=0; i<3; i++)
    {
        servo.servo_torque_set(i+1, true);
        usleep(10000);
        servo.setAngleInTime(i+1, offset[i]+1, 3000);
        usleep(10000);
        ROS_INFO("Servo_%d: torque ON", i+1);
    }

    sleep(5);

    for(i=0; i<3; i++)
    {
        servo.setAngleInTime(i+1, offset[i], 0);
    }

    ros::init(argc, argv, "vv_kuwamai_joint_state_subscriber");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("/vv_kuwamai/master_joint_state", 10, joint_callback);
    armjs = *(ros::topic::waitForMessage<sensor_msgs::JointState>("/vv_kuwamai/master_joint_state"));

    ros::Rate loop_rate(10);

    while (ros::ok())
    {
        for(i=0; i<3; i++)
        {
            js_ref = armjs.position[i] / PI * 180.0;
            js_diff = js_ref - theta[i];
            if (js_diff > js_vel) theta[i] += js_vel;
            else if (js_diff < -js_vel) theta[i] -= js_vel;
            else theta[i] = js_ref;
        }

        target[0] = theta[0];
        target[1] = -theta[1];
        target[2] = theta[2] + theta[1] - 90;

        for(i=0; i<3; i++)
        {
            //servo.move_target_degree(i+1, target[i] + offset[i]);
            servo.setAngleInTime(i+1, target[i] + offset[i], 100);
        }

        ros::spinOnce();
        loop_rate.sleep();
    }

    //servo.servo_torque_set(1, false);
    //servo.close_port();

    return 0;
}
