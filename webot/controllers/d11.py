from controller import Robot, Compass
from modules.differential import DifferentialKinematics
from math import atan2, pi
import matplotlib.pyplot as plt

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

'''
(w, l, h) = 0.08, 0.1, 0.03 meteres
wheel radius = 0.025 meters
wheel thickness = 0.01 meters
axle = distance b/w anchor points = 0.045 - (-0.045) = 0.09 meters
'''
DK = DifferentialKinematics(axle_length=0.09, radius=0.025)
predX = []
predY = []

left_motor = robot.getDevice('motor1')
right_motor = robot.getDevice('motor2')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# round and round
left_motor.setVelocity(3.0)
right_motor.setVelocity(6.0)

# getting the compass value which is set at center of the axle
compass = robot.getDevice('compass')
compass.enable(timestep)

lastTime = 0
duration = 120
while robot.step(timestep) != -1:
    [x, y, z] = compass.getValues()
    angle = atan2(y,x)

    DK.update(wl=3.0, wr=6.0, a=angle, dt=timestep/1000)

    current_time = robot.getTime()
    totalTime = current_time

    if current_time >= lastTime + 2:
        predX.append(DK.x)
        predY.append(DK.y)
        print(f"x: {DK.x:.2f} | y : {DK.y:.2f} | Angle : {DK.a:.2f}")
        lastTime = current_time

    if current_time >= duration:
        break



# plotting
print("=======================================================")
print("Now plotting the predictions.....")
plt.figure()
plt.scatter(predX, predY)
plt.title(f"Predicted X v/x Predicted Y after {duration / 60} minutes")
plt.grid(True)
plt.show()