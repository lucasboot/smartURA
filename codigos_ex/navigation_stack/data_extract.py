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

#System libs
import sys, select, termios, tty

arq = open("database.csv", "w")


moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
           }
speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

#Configuracoes basicas de velocidades
speed = .2
turn = 1

class data_extractor:
    image = CompressedImage()
    vel = np.array([0.0,0.0])
    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        self.subscriber1 = rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.callback1,  queue_size = 1)

    def callback1(self, ros_image):
        buffer = ros_image.data
        arq.write(str(buffer) + ", " + str(self.vel[0]) + ", " + str(self.vel[1]) +"\n")
        #print(buffer)

def main():
    '''Initializes and cleanup ros node'''
    settings = termios.tcgetattr(sys.stdin)
    ie = data_extractor()
    rospy.init_node('data_extractor', anonymous=True)

    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0

    publisher1 = rospy.Publisher("/cmd_vel", Twist, queue_size=5)
    try:
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                ie.vel[0] = x
                ie.vel[1] = th
                count = 0
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break
            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
            pub.publish(twist)

            #print("loop: {0}".format(count))
            #print("target: vx: {0}, wz: {1}".format(target_speed, target_turn))
            #print("publihsed: vx: {0}, wz: {1}".format(twist.linear.x, twist.angular.z))
    except Exception as e:
        print(e)
    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main()

arq.close()