#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

side = {
	'right': 0,
	'front': 0,
	'left': 0,
	}
mini = 0.3
maxi = 0.5
def callback(msg):
	global side
	side = {
	'right': min(msg.ranges[0:90]),
	'front': min(msg.ranges[91:269]),
	'left': min(msg.ranges[270:360]),
	}

def move():
	global side
	if 	side['left'] > mini and side['left'] < maxi and side['front'] > mini:
		return move_forward()
	if side['front'] < maxi:
		return move_right()
	if 	side['left'] > maxi :
		return move_left()
	if side['left'] < mini :
		return move_right()
	#else: return Twist()


def move_forward():
	msg = Twist()
	msg.linear.x = 0.5
	msg.angular.z = 0
	return msg

def move_right():
	msg = Twist()
	msg.linear.x = 0
	msg.angular.z = -0.5
	return msg

def move_left():
	msg = Twist()
	msg.linear.x = 0
	msg.angular.z = 0.5
	return msg

rospy.init_node('poyekhavshiy')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)


while not rospy.is_shutdown():
	msg = move()
	pub.publish(msg)
