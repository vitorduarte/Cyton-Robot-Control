#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Responde evento não controlável 'done' após

import rospy
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import Int8
from std_msgs.msg import String

movement =[
[# redLoad
	[0, 0, 0, 0, 0, 0, 0, 0], #starts
	[0, 0, 0, 45, 0, -75, 0, 45], #prepares
	[0, -60, 0, 45, 0, -75, 0, 45], #lows
	[0, -60, 0, 45, 0, -75, 0, 0], #locks
	[0, 0, 0, 0, 0, 0, 0, 0], #initial
	[-45, 0, 0, 45, 0, -75, 0, 0], #prepares
	[-45, -60, 0, 45, 0, -75, 0, 0], #lows
	[-45, -60, 0, 45, 0, -75, 0, 45], #unlock
	[-45, 0, 0, 45, 0, -75, 0, 45], #rises
	[0, 0, 0, 0, 0, 0, 0, 45], #finishes
],
[# greenLoad
	[0, 0, 0, 0, 0, 0, 0, 0], #starts
	[0, 0, 0, 45, 0, -75, 0, 45], #prepares
	[0, -60, 0, 45, 0, -75, 0, 45], #lows
	[0, -60, 0, 45, 0, -75, 0, 0], #locks
	[0, 0, 0, 0, 0, 0, 0, 0], #initial
	[-80, 0, 0, 45, 0, -75, 0, 0], #prepares
	[-80, -60, 0, 45, 0, -75, 0, 0], #lows
	[-80, -60, 0, 45, 0, -75, 0, 45], #unlock
	[-80, 0, 0, 45, 0, -75, 0, 45], #rises
	[0, 0, 0, 0, 0, 0, 0, 0], #finishes
],
[# redUnload
	[0, 0, 0, 0, 0, 0, 0, 0], #starts
	[-45, 0, 0, 45, 0, -75, 0, 45], #prepares
	[-45, -60, 0, 45, 0, -75, 0, 45], #lows
	[-45, -60, 0, 45, 0, -75, 0, 0], #locks
	[0, 0, 0, 0, 0, 0, 0, 0], #initial
	[45, 0, 0, 45, 0, -75, 0, 0], #prepares
	[45, -60, 0, 45, 0, -75, 0, 0], #lows
	[45, -60, 0, 45, 0, -75, 0, 45], #unlock
	[0, 0, 0, 0, 0, 0, 0, 0], #finishes
],
[# greenUnload
	[0, 0, 0, 0, 0, 0, 0, 0], #starts
	[-80, 0, 0, 45, 0, -75, 0, 45], #prepares
	[-80, -60, 0, 45, 0, -75, 0, 45], #lows
	[-80, -60, 0, 45, 0, -75, 0, 0], #locks
	[0, 0, 0, 0, 0, 0, 0, 0], #initial
	[45, 0, 0, 45, 0, -75, 0, 0], #prepares
	[45, -60, 0, 45, 0, -75, 0, 0], #lows
	[45, -60, 0, 45, 0, -75, 0, 45], #unlock
	[0, 0, 0, 0, 0, 0, 0, 0], #finishes
],
[# red2Green
	[0, 0, 0, 0, 0, 0, 0, 0], #starts
	[-45, 0, 0, 45, 0, -75, 0, 45], #prepares
	[-45, -60, 0, 45, 0, -75, 0, 45], #lows
	[-45, -60, 0, 45, 0, -75, 0, 0], #locks
	[-80, 0, 0, 0, 0, 0, 0, 0], #initial
	[-80, 0, 0, 45, 0, -75, 0, 0], #prepares
	[-80, -60, 0, 45, 0, -75, 0, 0], #lows
	[-80, -60, 0, 45, 0, -75, 0, 45], #unlock
	[-80, 0, 0, 45, 0, -75, 0, 45], #rises
	[0, 0, 0, 0, 0, 0, 0, 0], #finishes
]
]


def moveCallback(move):
	global pubPose
	global pubEvent

	print('movement started')
	for pose in movement[move.data]:
		poseToSend = Int8MultiArray()
		poseToSend.data = pose	
		print(poseToSend)
		pubPose.publish(poseToSend)
		rospy.sleep(3)

	print('movement finished')
	eventToSend = String()
	eventToSend = 'cytonIdle'
	pubEvent.publish(eventToSend)

def main():
	global pubPose
	global pubEvent

	rospy.init_node('posePublisher', anonymous=False)
	pubPose = rospy.Publisher('pose', Int8MultiArray, queue_size = 10)
	pubEvent = rospy.Publisher('event', String, queue_size = 10)
	rospy.Subscriber('move', Int8, moveCallback)

	while not rospy.is_shutdown():
		pass




if __name__ == '__main__':
	main()