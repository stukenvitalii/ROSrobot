#! /usr/bin/env python

import rospy
from math import atan2, pi
from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import LaserScan


def laser_callback(data):
    global lasers_range
    lasers_range = data.ranges


def avoid_obstcls():
    if lasers_range[1] < 1:
        print("obstacle")
        for i in range(200):
            cmd.linear.x = 0
            cmd.angular.z = pi / 2 / 2
            pub.publish(cmd)
            rate.sleep()
        print("step 1")
        while lasers_range[0] < 10:
            cmd.linear.x = 0.5
            cmd.angular.z = 0
            pub.publish(cmd)
            rate.sleep()
        print("step 2")
        for i in range(350):
            cmd.angular.z = -pi / 2 / 4
            pub.publish(cmd)
            rate.sleep()
        print("step 3")
        for i in range(250):
            cmd.angular.z = 0
            cmd.linear.x = 0.5
            pub.publish(cmd)
            rate.sleep()
        print("step 4")
        cmd.angular.z = 0
        cmd.linear.x = 0.5


def printInfo():
    global x
    global y

    print(f"Position:\n\tx: {x:.5f}\n\ty: {y:.5f}\n")


def getState(name):
    global x
    global y
    global theta

    modelCoord = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
    respCoord = modelCoord(str(name), 'world')

    rot_q = respCoord.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    x = respCoord.pose.position.x
    y = respCoord.pose.position.y


pub = rospy.Publisher('/part2_cmr/cmd_vel', Twist, queue_size=10)
rospy.init_node('command_node', anonymous=True)
rospy.Subscriber("/bot_0/laser/scan", LaserScan, laser_callback)

rate = rospy.Rate(100)

cmd = Twist()

xInput = float(input('Input x: '))
yInput = float(input('Input y: '))
print('\n')

getState('rosbots')
printInfo()

while not rospy.is_shutdown():
    deltaX = xInput - x
    deltaY = yInput - y

    angle_to_goal = atan2(deltaY, deltaX)
    avoid_obstcls()

    if abs(angle_to_goal - theta) > 0.2:
        for i in range(250):
            cmd.angular.z = (angle_to_goal - theta)/2.5
            cmd.linear.x = 0
            pub.publish(cmd)
            rate.sleep()
    else:
        cmd.angular.z = 0.0
        cmd.linear.x = 0.5

    if abs(deltaX) < 0.2 and abs(deltaY) < 0.2:
        break

    getState('rosbots')
    pub.publish(cmd)
    rate.sleep()

cmd = Twist()
pub.publish(cmd)

printInfo()
