#!/usr/bin/env python3

import numpy as np
import rospy
import roslib
import subprocess
import time
from geometry_msgs.msg  import Twist
import cv2
import mediapipe as mp
from math import dist
    
class hand_gesture_controller():
  
  def __init__(self):
    rospy.init_node('hand_gesture_controller', anonymous=False)
    self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    self.rate = rospy.Rate(10)
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_drawing_styles = mp.solutions.drawing_styles
    self.mp_hands = mp.solutions.hands
    self.vel_msg = Twist()

    
  def controlCommad(self):
    cap = cv2.VideoCapture(0)
    with self.mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
  
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame")
          continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
  
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      
        if results.multi_hand_landmarks:	
          landmarks = results.multi_hand_landmarks[0]
          
          if landmarks.landmark[12].x < 0.34: self.vel_msg.angular.z = -1.2
          elif landmarks.landmark[12].x > 0.67: self.vel_msg.angular.z = 1.2
          else: self.vel_msg.angular.z = 0
          
          width = dist([landmarks.landmark[3].x, landmarks.landmark[3].y], [landmarks.landmark[17].x, landmarks.landmark[17].y]) 
          height = dist([landmarks.landmark[12].x, landmarks.landmark[12].y], [landmarks.landmark[0].x, landmarks.landmark[0].y]) 

          if abs(width) / abs(height) > 0.6:
            self.vel_msg.linear.x = 0.3 
          else:
            self.vel_msg.linear.x = 0
          
          self.velocity_publisher.publish(self.vel_msg)
          
          for hand_landmarks in results.multi_hand_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())
     
        cv2.line(image, (image.shape[1]//3, 0), (image.shape[1]//3, image.shape[0]), (255,0,0), 5) 
        cv2.line(image, (2*image.shape[1]//3, 0), (2*image.shape[1]//3, image.shape[0]), (255,0,0), 5) 
   
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(10) & 0xFF == ord("q"): 
          break

        self.rate.sleep()

    cap.release()
    return None
    
    
if __name__ == "__main__":

  handGestureContoller = hand_gesture_controller()
  handGestureContoller.controlCommad()
  
  
  
