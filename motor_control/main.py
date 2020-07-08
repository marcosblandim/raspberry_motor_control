import RPi.GPIO as gpio
import collections

class Motors():
    """
    Controls two motors wich follows the engine/H-bridge circuit design,
    described in https://github.com/marcosblandim/raspberry_motor_control.
    # Usage

        You can set the speed of each motor by changing the properties left speed and right speed.
        Its speed can vary from -100 to 100. Note that the sign indicates the direction of rotation. 
        Note: you shouldn't have more than one instance at time.
    """
    
    # initialize instance.
    def __init__(self, left_pin_engine, left_pin_H_bridge, right_pin_engine, right_pin_H_bridge, *, pwm_frequency=60, initial_speeds=(0,0), pin_mode="BCM", set_warnings=False):
        
        # motor class.
        Motor = collections.namedtuple("Motor", "engine h_bridge")
        
        # public attributes.
        self.left_motor = Motor(left_pin_engine, left_pin_H_bridge)
        self.right_motor = Motor(right_pin_engine, right_pin_H_bridge)
        # private attributes.
        self.__left_speed, 
        self.__right_speed = initial_speeds
        
        # set warnings.
        gpio.setwarnings(set_warnings)

        # set pin mode.
        pin_mode_upper = pin_mode.upper()
        if pin_mode_upper == "BCM":
            self.__pin_mode = gpio.BCM
        if pin_mode_upper == "BOARD":
            self.__pin_mode = gpio.BOARD
        if (pin_mode_upper != "BCM") and (pin_mode_upper != "BOARD"):
            self.__pin_mode = pin_mode
        gpio.setmode(self.__pin_mode)

        # setuop H-bridge motors.
        gpio.setup(self.left_motor.h_bridge, gpio.OUT)
        gpio.setup(self.right_motor.h_bridge, gpio.OUT)
        # setup engine motors.
        self.__left_motor_pwm   = gpio.PWM(self.left_motor.engine, pwm_frequency)
        self.__right_motor_pwm  = gpio.PWM(self.right_motor.engine, pwm_frequency)
        # initialize motors.
        self.__left_motor_pwm.start(0)
        self.__right_motor_pwm.start(0)
        self.move(*initial_speeds)

        super().__init__()
    
    def __del__(self):
        self.close()

    # abstract general moving.
    def move(self, left_speed, right_speed):
        """
        Sets the speed of both motors.
        """
        self.left_speed = left_speed        
        self.right_speed = right_speed

    # handle the speed of the left motor.
    def set_left_speed(self, speed):
        # stop engine if changing directions.
        if (speed < 0) != (self.__left_speed < 0):
            self.__left_motor_pwm.ChangeDutyCycle(0)
        # set directions.
        gpio.output(self.left_motor.engine, speed > 0)
        # set speed.
        self.__left_motor_pwm.ChangeDutyCycle(abs(speed))
        # update private attribute.
        self.__left_speed = speed

    def get_left_speed(self):
        return self.__left_speed

    left_speed = property(get_left_speed, set_left_speed, doc="the speed of the left motor.")

    # handle the speed of the right motor.
    def set_right_speed(self, speed):
        # stop engine if changing directions.
        if (speed < 0) != (self.__right_speed < 0):
            self.__right_motor_pwm.ChangeDutyCycle(0)
        # set directions.
        gpio.output(self.right_motor.engine, speed > 0)
        # set speed.
        self.__right_motor_pwm.ChangeDutyCycle(abs(speed))
        # update private attribute.
        self.__right_speed = speed

    def get_right_speed(self):
        return self.__right_speed

    right_speed = property(get_right_speed, set_right_speed, doc="the speed of the right motor.")
    
    # handle cleanup.
    def clean_motors(self):
        gpio.cleanup(self.left_motor.engine)
        gpio.cleanup(self.left_motor.h_bridge)
        gpio.cleanup(self.right_motor.engine)
        gpio.cleanup(self.right_motor.h_bridge)

    @staticmethod
    def close():
        gpio.cleanup()
