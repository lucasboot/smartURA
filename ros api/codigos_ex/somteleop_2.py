import rospy
from geometry_msgs.msg import Twist
import sys, time
import numpy as np
# Ros libraries
import roslib
import pandas as pd
# Ros Messages
from sensor_msgs.msg import LaserScan
from scipy.spatial import distance

class laser_feature:
    #COLOCAR AQUI A IMPORTACAO DO CSV COM OS NEURONIOS
   neuronios = pd.read_csv("")
    ######
   
   key = 1
   def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        self.subscriber = rospy.Subscriber("/kobuki/laser/scan", LaserScan, self.callback,  queue_size = 1)
   def callback(self, ros_data):
        novodado = ros_data.ranges
        ds = []
        ##INSERIR A LOGICA PARA DETERMINACAO DO NEURONIO VENCEDOR PARA A REDE DE NEURONIOS TREINADA




        ######
  
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

speed = .4
turn = 1
if __name__=="__main__":
    rospy.init_node('turtlebot_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    ic = laser_feature()
    try:
        while(1):
            if(ic.key == 1):
                key = 'i'
            elif (ic.key == 0):
                key = 'j'
            else:
                key = 'l'
            print(key)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
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
    except Exception as e:
        print(e)
    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

