"""d9 controller."""
from controller import Robot, Supervisor
from PID import PIDController
from realtime_plot import RealTimePlotter

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())
objectPID = PIDController(kp=0.03, ki=0.5, kd=0.001)
linePID = PIDController(kp=0.03, ki=0.5, kd=0.001)

plotter = RealTimePlotter()

# initialise the motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# front object sensor
ps0 = robot.getDevice('ps0')
ps1 = robot.getDevice('ps7')
ps0.enable(timestep)
ps1.enable(timestep)

# infrared sensor
ir0 = robot.getDevice('ir0')
ir1 = robot.getDevice('ir1')
ir0.enable(timestep)
ir1.enable(timestep)

# movement
def objMovement(control):
    speed = min(abs(control), 6.0)
    dir = -1 if control < 0 else 1 
    left_motor.setVelocity(-speed*dir)
    right_motor.setVelocity(-speed*dir)

def linMovement(control):
    global ctrl, speed
    ctrl = max(min(control, 3), -3)
    speed = 2
    left_motor.setVelocity(speed - ctrl)
    right_motor.setVelocity(speed + ctrl)

testDuration = 0.5
testStartT = -1

while robot.step(timestep) != -1:
    currTime = robot.getTime()
    dt = timestep/1000

    # <-------------------- line folow -------------------->
    rightIR = ir0.getValue()
    leftIR = ir1.getValue()
    threshold = 600



    leftOfLine = leftIR > threshold
    rightOfLine = rightIR > threshold

    if leftOfLine and not rightOfLine:
        linError = 1
    elif not leftOfLine and rightOfLine:
        linError = -1
    elif leftOfLine and rightOfLine:
        linError = 0
    else:
        linError = 0


    # <----- heuristic methods ----->
    # linePID.tune(kp=1.8, ki=0.00, kd=1.8)
    # linControl, linP, linI, linD = linePID.heuristicPID(error=linError, dt=dt)
    # <----------------------------->

    # <------ ziegler nichols ------------>
    zn_initialise = True
    linePID.tune(kp=2, ki=0.00, kd=0)
    linControl, linP, linI, linD = linePID.znPID(
        error=linError,
        dt=dt,
        init=zn_initialise,
        KU=2,
        TU=0.1
    )


    plotter.add_data(robot.getTime(), linError, linControl)
    linMovement(linControl)

    if currTime - testStartT  >= testDuration:
        print(f"T:{currTime:.2f} | leftIR:{leftIR:.1f} | rightIR:{rightIR:.1f} | Err:{linError:.3f} | Control :{linControl:.3f}")
        testStartT = currTime

    # <---------------------------------------------------->

plotter.close()