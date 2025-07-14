"""d7 controller."""
from controller import Robot
import math

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Get motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# calibration =====================================================
def calibrateDistance():
    print("Measuring forward speed...")
    startPos = robot.getTime()
    left_motor.setVelocity(6.0)
    right_motor.setVelocity(6.0)
    start = robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime() - start > 3.0:
            stop()
            break

def calibrateAngle():
    print("Measuring rotation...")
    compensation = 0.07 
    start = robot.getTime()
    left_motor.setVelocity(6.0)
    right_motor.setVelocity(-6.0)
    start = robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime() - start +compensation > 2.0:
            stop()
            break
# ===============================================================

v = 0.25    # distance per second
omega = 75  # degrees per second
length = 0.5

def stop():
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

def moveForward(distance):
    seconds = distance/v
    start = robot.getTime()

    left_motor.setVelocity(6.0)
    right_motor.setVelocity(6.0)

    while robot.step(timestep) != -1:
        if robot.getTime() - start > seconds:
            stop()
            break

def rotateDegrees(angle):
    compensation = 0.6
    seconds = abs(angle) / omega + compensation
    start = robot.getTime()

    dir = 1 if angle > 0 else -1
    left_motor.setVelocity(-6.0 * dir)
    right_motor.setVelocity(6.0 * dir)

    while robot.step(timestep) != -1:
        if robot.getTime() - start > seconds:
            stop()
            break 

def pattern():
    # first triangle
    moveForward(0.5)
    rotateDegrees(90)
    moveForward(0.5)
    rotateDegrees(90+45)
    moveForward(0.7)

    #second triangle
    rotateDegrees(-90)
    moveForward(0.7)
    rotateDegrees(90+45)
    moveForward(0.5)
    rotateDegrees(90)
    moveForward(0.5)

# ===============================================================

startTime = robot.getTime()
while robot.step(timestep) != -1:
    pattern()
    stop()
    break