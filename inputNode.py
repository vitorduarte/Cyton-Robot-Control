#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import random
from std_msgs.msg import String


def main():
	rospy.init_node('inputNode', anonymous = True)
	pub = rospy.Publisher('event', String, queue_size = 10)
	
	while True:
		newInput = raw_input('Novo evento (redNew/greenNew/redDone/greenDone/greenLoad/greenUnload/redLoad/redUnload/break): ')
		if newInput == 'break':
			print('Closing node')
			break
		else:
			inputToSend = String()
			inputToSend = newInput
			print(inputToSend)
			pub.publish(inputToSend)


if __name__ == '__main__':
	main()