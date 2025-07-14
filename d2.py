import  pybullet as p
import time, math
import pybullet_data, gym

from collections import UserDict
registry = UserDict(gym.envs.registration.registry)
registry.env_specs = gym.envs.registration.registry
gym.envs.registration.registry = registry

# --------------------------------------------------------------

# initial setup
client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # for built-in models
p.setGravity(0, 0, -9.81)
plane = p.loadURDF("plane.urdf", useFixedBase=True)
car = p.loadURDF("urdfs/car.urdf", basePosition=[0, 0, 0.5])


jointsN = p.getNumJoints(car)
print(f"car has {jointsN} joints")
# ---------- UNDERSTANDING MY CAR -----------------
# for i in range(joints):
#     info = p.getJointInfo(car, i)
#     print(f"num {i} - {info[1].decode('utf-8')}")
#     print(f"type: {info[2]}")
#     print(f"movable: {info[2] != p.JOINT_FIXED}")
#     print("\n")
# --------------------------------------------------

# getting all the movable joints
movable_joints = []
for i in range(jointsN):
    info = p.getJointInfo(car, i)
    if info[2] != p.JOINT_FIXED:
        movable_joints.append(i)

# dancing function
def dance():
    t = time.time()

    for i, joint in enumerate(movable_joints):

        if i%3 == 0:
            angle = math.sin(t*2 + i)*0.5
        elif i%3 == 1:
            angle = math.cos(t*3 + i)*0.5
        else:
            angle = math.sin(t*4)*math.cos(t*2)*0.5

        p.setJointMotorControl2(
            car,
            joint,
            p.POSITION_CONTROL,
            targetPosition=angle,
            force=5
        )
    time.sleep(0.01)

try:
    while True:
        p.setRealTimeSimulation(1)
        dance()
except KeyboardInterrupt:
    p.disconnect()