'''
This implements a trackbar motor controller.
Important note: Opencv module is required for this code to run.
'''

import numpy as np
import cv2

from motor_control import Motors


LEFT_ENGINE_PIN = 12
LEFT_H_BRIDGE_PIN = 16
RIGHT_ENGINE_PIN = 20
RIGHT_H_BRIDGE_PIN = 21

motors = Motors(LEFT_ENGINE_PIN, LEFT_H_BRIDGE_PIN, RIGHT_ENGINE_PIN, RIGHT_H_BRIDGE_PIN)

# Create a black image and a window
empty_iamge = np.zeros((1,1,1), np.uint8)
cv2.namedWindow('empty window')

# create trackbars for color change
cv2.createTrackbar('Left speed',    'empty window',-100,100,lambda: None)
cv2.createTrackbar('Right speed',   'empty window',-100,100,lambda: None)

while(True):
    
    cv2.imshow('empty window',empty_iamge)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    motors.left_speed =  cv2.getTrackbarPos('Left speed',   'empty window')
    motors.right_speed = cv2.getTrackbarPos('Right speed',  'empty window')
