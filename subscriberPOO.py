#!/usr/bin/env python

# Python libs
import sys, time
import numpy as np
# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import LaserScan

class laser_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        #self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage)
        # self.bridge = CvBridge()
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/kobuki/laser/scan",
            LaserScan, self.callback,  queue_size = 1)

    def callback(self, ros_data):
        np_arr = ros_data.ranges
        # Publish new info
        #self.image_pub.publish(msg)
        #self.subscriber.unregister()

def main(args):
    '''Initializes and cleanup ros node'''
    ic = laser_feature()
    rospy.init_node('laser_ranges', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS module")

if __name__ == '__main__':
    main(sys.argv)