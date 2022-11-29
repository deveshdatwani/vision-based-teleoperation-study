#!/usr/bin/env python3

import numpy as np
import rospy
import roslib
import subprocess
import time
from geometry_msgs.msg  import Twist
from sensor_msgs.msg import Joy



class robot():
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.pose_subscriber2 = rospy.Subscriber('/joy', Joy, self.callback)
        self.rate = rospy.Rate(20)
        self.incoming = False
        
    def callback(self, data):
        print(data.axes)
        self.incoming = True
        self.linear = data.axes[1]
        self.angular = data.axes[0]
        print(self.linear)
        print(self.angular)

    def moving(self,vel_msg):
        self.velocity_publisher.publish(vel_msg)
        self.incoming = False

data=Joy()
vel_msg=Twist()
turtle = robot()

if __name__ == '__main__':
    while True:
        if turtle.incoming:
            vel_msg.linear.x = turtle.linear * 0.3
            vel_msg.angular.z = turtle.angular * 1.2
            turtle.moving(vel_msg)
            turtle.rate.sleep()
    
