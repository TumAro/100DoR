from controller import Robot
from math import sin, cos, pi
import tkinter as tk
from modules.transformation import Transformation3D

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

n = robot.getNumberOfDevices()

# initialising the joints
joints = []
for i in range(n):
    joint = robot.getDeviceByIndex(i)
    if joint.getNodeType() == 57:
        joint.setPosition(0)
        joints.append(joint)
n = len(joints)

print(joints)

# links
links = [
    151.8,  # base -> shoulder
    243.5,  # shoulder -> elbow
    213.2,  # elbow -> wrists
    85.35,  # wrist1 -> wrist2
    131.05, # rotation axis -> flange (combines offset of wrist 1 and 2 while the flange is too close to wrist 2)
]

vec = [0,0,0]

# transformation
A = Transformation3D()

# initialising the sliders
root = tk.Tk()
sliders = []

def on_click():
    print(f"x: {vec[0]/1000:.2f}    | y: {vec[1]/1000:.2f}  | z: {vec[2]/1000:.2f}", flush=True)


for i in range(n):
    slider = tk.Scale(root, from_= 2*pi, to= -2*pi, resolution=0.01,label=f"{joints[i].getName()}", orient=tk.HORIZONTAL, length=300)
    slider.pack()
    sliders.append(slider)

tk.Button(root, text="Calc Fwd Kin", command=on_click).pack()

while robot.step(timestep) != -1:
    root.update()
    dt = robot.getTime() / 1000
    angles = []
    for i, joint in enumerate(joints):
        angle = sliders[i].get()
        angles.append(angle)
        joint.setPosition(angle)

    A._reset()
    '''A.Rz(angles[0]).T([0,0,links[0]]).Rx(angles[1]).T([links[1],0,0]).Rx(angles[2]).T([links[2],0,0]).Rx(angles[3]).T([links[3],0,0]).Ry(angles[4]).Rx(angles[5]).T([0,0,links[4]])
    # base Rz -> Tz -> shoulder Rx -> Tx -> elbow Rx -> Tx -> wrist 1 Rx -> Tx -> wrist 2 Ry -> wrist 3 Rx -> Tz for flange offset
    # in the end we directly rotate from Wrist 2 to 3 cause UR series in made in such a way that their axis intersect'''

    # Base(J1 Z rot) -> Shoulder(J2 Y rot) -> Elbow(J3 Y rot) -> Wrist1(J4 Y rot) -> Wrist2(J5 Z rot) -> Wrist3(J6 Y rot) -> Flange
    A.Rz(angles[0]).T([0, 0, links[0]]) \
    .Ry(angles[1]).T([links[1], 0, 0]) \
    .Ry(angles[2]).T([links[2], 0, 0]) \
    .Ry(angles[3]).T([0, 0, links[3]]) \
    .Rz(angles[4]).T([0, 0, 0]) \
    .Ry(angles[5]).T([0, 0, links[4]])


    vec = A._getPos()

    