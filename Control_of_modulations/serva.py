import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

# Set GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
pin_number = 8  # Replace with the appropriate pin number

# Set up the GPIO pin for servo motor
GPIO.setup(pin_number, GPIO.OUT)
pwm = GPIO.PWM(pin_number, 50)  # PWM frequency of 50Hz
pwm.start(0)  # Start PWM with 0% duty cycle

# Function to set the servo position based on the angle
def set_servo_position(angle):
    duty_cycle = (angle / 18) + 2.5  # Calculate duty cycle for the given angle
    pwm.ChangeDutyCycle(duty_cycle)


# Main program loop
try:
    while True:

        angl = float(input())
        set_servo_position(angl)

        time.sleep(0.1)  # Delay to allow the servo to move

except KeyboardInterrupt:
    pass

# Stop PWM and clean up GPIO
pwm.stop()
GPIO.cleanup()
