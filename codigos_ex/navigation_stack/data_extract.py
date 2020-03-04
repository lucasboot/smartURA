#!/usr/bin/env python

# Python libs
import numpy as np
# Ros libraries
import roslib
import rospy
import time

# Ros Messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist


class data_extractor:
    image = CompressedImage()
    vel = Twist()
    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        self.subscriber1 = rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.callback1,  queue_size = 1)
        self.subscriber2 = rospy.Subscriber("/cmd_vel", Twist, self.callback2, queue_size=1)

    def callback1(self, ros_image):
        buffer = ros_image.data
        #print(buffer)
    
    def callback2(self, ros_twist):
        vel_linear = ros_twist.linear
        vel_angular = ros_twist.angular 
        print(vel_linear, " \n")

        # Publish new info
        #self.image_pub.publish(msg)
        #self.subscriber.unregister()

def main():
    '''Initializes and cleanup ros node'''
    ie = data_extractor()
    rospy.init_node('data_extractor', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS module")

if __name__ == '__main__':
    main()
