from controller import Robot
from modules.PID import PIDController

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('motor1')
right_motor = robot.getDevice('motor2')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

PID = PIDController()


sensors = [robot.getDevice("ds_front"), robot.getDevice("ds_right"), robot.getDevice("ds_left")]

'''
(w, l, h) = 0.08, 0.1, 0.03 meteres
wheel radius = 0.025 meters
wheel thickness = 0.01 meters
axle = distance b/w anchor points = 0.045 - (-0.045) = 0.09 meters
'''

FRONT_THRESHOLD = 10    # from the front
MAX_CORRECTION = 2      # steering adjustment
REVERSE_THRESHOLD = 2.0
SIDE_STUCK_THRESHOLD = 2.0

def movement(control: float):
    base = 3.0

    # if abs(control) < 0.05:
    #     left_motor.setVelocity(base)
    #     right_motor.setVelocity(base)
    #     return

    vel = max(min(control,2.0), -2.0)
    # vel = control
    # dir = -1 if control < 0 else 1

    leftVel = base + vel
    rightVel = base - vel

    # print(f"base : {base:.2f} | left : {leftVel:.2f} | right : {rightVel:.2f}")
    left_motor.setVelocity(leftVel)
    right_motor.setVelocity(rightVel)

for sensor in sensors:
    sensor.enable(timestep)


PID.tune(
            kp=0.28,
            ki=0.0056,
            kd=0.00
        )
while robot.step(timestep) != -1:
    dt = timestep/1000

    front_distance = sensors[0].getValue()/ 100

    right_distance = sensors[1].getValue()/ 100
    left_distance = sensors[2].getValue()/100

    

    # ----------------------------------
    cap = 9
    right_c = min(right_distance, cap)
    left_c = min(left_distance, cap)
    print(f"right {right_c} | left {left_c}")
    both_walls = (right_distance < cap) and (left_distance < cap)
    # ----------------------------------

    if front_distance < REVERSE_THRESHOLD:
        left_motor.setVelocity(-1.5)
        right_motor.setVelocity(-2.0)
        continue

        
    elif front_distance < FRONT_THRESHOLD:
        error = (FRONT_THRESHOLD - front_distance) * 3.0
        if both_walls:
            error += (right_c - left_c)
        # print(error)
    else:
        error = (right_c - left_c) / 2 if both_walls else 0.0
        

    
    control, _, _, _ = PID.heuristicPID(error=error, dt=dt)
    
    movement(control)