#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist


pub = rospy.Publisher('/part2_cmr/cmd_vel', Twist, queue_size=10)
rospy.init_node('command_node', anonymous=True)
rate = rospy.Rate(10)  # 10hz
cmd = Twist()
cmd.linear.x = 0.5
for i in range(100):
    pub.publish(cmd)
    rate.sleep()
cmd = Twist()
pub.publish(cmd)
