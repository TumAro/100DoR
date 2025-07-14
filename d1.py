import  pybullet as p
import time, inputs

import gym
from collections import UserDict
registry = UserDict(gym.envs.registration.registry)
registry.env_specs = gym.envs.registration.registry
gym.envs.registration.registry = registry


client = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

plane = p.loadURDF("urdfs/plane.urdf", basePosition=[0, 0, 0], useFixedBase=True, physicsClientId=client)
cube = p.loadURDF("urdfs/cube.urdf", basePosition=[0, 0, 1.5], physicsClientId=client)


speed = 10.0

def control():
    keys = p.getKeyboardEvents(physicsClientId=client)
    for key, state in keys.items():
        if state & p.KEY_IS_DOWN:
            print(f'{key}')
            if key == 119:  # 'W' key
                p.applyExternalForce(cube, -1, forceObj=[0, 0, speed], posObj=[0, 0, 0], flags=p.WORLD_FRAME, physicsClientId=client)
            elif key == 115:  # 'S' key
                p.applyExternalForce(cube, -1, forceObj=[0, 0, -speed], posObj=[0, 0, 0], flags=p.WORLD_FRAME, physicsClientId=client)
            elif key == 97:  # 'A' key
                p.applyExternalForce(cube, -1, forceObj=[-speed, 0, 0], posObj=[0, 0, 0], flags=p.WORLD_FRAME, physicsClientId=client)
            elif key == 100:  # 'D' key
                p.applyExternalForce(cube, -1, forceObj=[speed, 0, 0], posObj=[0, 0, 0], flags=p.WORLD_FRAME, physicsClientId=client)


try:
    while True:  # Simulate for 240 steps
        control()
        p.stepSimulation(physicsClientId=client)
        time.sleep(1 / 240)  # Simulate at 240Hz
except KeyboardInterrupt:
    pass

p.disconnect()