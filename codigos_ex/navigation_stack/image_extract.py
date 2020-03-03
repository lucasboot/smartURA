#!/usr/bin/env python

# Python libs
import numpy as np
# Ros libraries
import roslib
import rospy
import time

# Ros Messages
from sensor_msgs.msg import CompressedImage

class image_extractor:
    image = CompressedImage()
    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        self.subscriber = rospy.Subscriber("/camera/rgb/image_raw/compressed",
            CompressedImage, self.callback,  queue_size = 1)

    def callback(self, ros_data):
        buffer = ros_data.data
        print(buffer)


        # Publish new info
        #self.image_pub.publish(msg)
        #self.subscriber.unregister()

def main(args):
    '''Initializes and cleanup ros node'''
    ie = image_extractor()
    rospy.init_node('image_extractor', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS module")

if __name__ == '__main__':
    main()
