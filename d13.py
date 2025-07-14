from controller import Robot
from modules.PID import PIDController

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('motor2')
right_motor = robot.getDevice('motor1')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

wall_PID = PIDController()
turn_PID = PIDController()


sensors = [robot.getDevice("ds_front"), robot.getDevice("ds_right"), robot.getDevice("ds_left")]
for sensor in sensors:
    sensor.enable(timestep)

'''
(w, l, h) = 0.08, 0.1, 0.03 meteres
wheel radius = 0.025 meters
wheel thickness = 0.01 meters
axle = distance b/w anchor points = 0.045 - (-0.045) = 0.09 meters
'''

def movement(control: float, dir=1, base= 3.0):
    vel = max(min(control,base), -base)
    # vel = control

    leftVel = base - vel*dir
    rightVel = base + vel*dir

    # print(f"base : {base:.2f} | left : {leftVel:.2f} | right : {rightVel:.2f}")
    left_motor.setVelocity(leftVel)
    right_motor.setVelocity(rightVel)

def dontMove():
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

wall_PID.tune(
    kp=0.49,
    ki=0.01,
    kd=0.049
)

turn_PID.tune(
    kp=0.56,
    ki=0.0,
    kd=0.056
)

turning = False
while robot.step(timestep) != -1:
    dt = timestep/1000

    front = sensors[0].getValue()/ 100
    right = sensors[1].getValue()/ 100
    left = sensors[2].getValue()/ 100

    print(f"err:  | front: {front:.2f} | left: {left:.2f} | right : {right:.2f}")
    
    if front < 4.0:

        # reset I term and alignment error
        turn_PID.reset()
        error = right - left
        dir = -1 if error> 0 else 1


        
        control, *_ = turn_PID.heuristicPID(error=error, dt=dt)
        movement(control, dir, base=1.5)
        continue
        

    # else:
    error = right - left
    control, _, _, _ = wall_PID.heuristicPID(error=error, dt=dt)
    movement(control)
        # dontMove()

