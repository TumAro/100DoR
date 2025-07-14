"""d8 controller."""

from controller import Robot, DistanceSensor

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# initialise the motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# initialising the sensors
ps = [robot.getDevice(f'ps{i}') for i in range(8)]
for i in range(8):
    ps[i].enable(timestep)

# motor control
def movement(baseSpeed, control):
    speed = min(abs(control), 6.0)
    dir = -1 if control < 0 else 1 
    left_motor.setVelocity(-speed*dir)
    right_motor.setVelocity(-speed*dir)

# pid 
kp, ki, kd = 0.03, 0.5, 0.001
integral = 0
prevError = 0

target = 80

def pidController(current):
    global integral, prevError
    error = current - target
    
    P = kp * error

    dt = timestep/1000.0
    integral = integral + error*dt
    I = ki * integral

    derivative = (error - prevError) / dt
    D = kd * derivative
    prevError = error

    control = P+I+D
    movement(0, control)

    if robot.getTime() % 1 < 0.02:
        print(f"distance: {frontDistance:.2f}")
        print(f"error: {error:.2f}, P: {P:.2f}, I: {I:.2f}, D: {D:.2f}")

# Main loop:
while robot.step(timestep) != -1:

    rightPS = ps[0].getValue()
    leftPS = ps[-1].getValue()

    frontDistance = (rightPS+leftPS)/2
    pidController(frontDistance)
