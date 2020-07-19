'''
Makes the robot turn clockwise and counter-clockwise
for 2 seconds each and stops.
'''

from time import sleep

from motor_control import Motors


LEFT_ENGINE_PIN = 12
LEFT_H_BRIDGE_PIN = 16
RIGHT_ENGINE_PIN = 20
RIGHT_H_BRIDGE_PIN = 21

motors = Motors(LEFT_ENGINE_PIN, LEFT_H_BRIDGE_PIN, RIGHT_ENGINE_PIN, RIGHT_H_BRIDGE_PIN)

motors.move(60,-60)
sleep(2)

motors.move(-60,60)
sleep(2)

motors.stop()
motors.close()
