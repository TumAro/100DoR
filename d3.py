import mujoco
import mujoco.viewer
import numpy as np
import keyboard
# from mujoco_models import sphere

model = mujoco.MjModel.from_xml_path("xmls/obstacles.xml")
data = mujoco.MjData(model)
# print(f"{type(model)}, {type(data)}")


def reset(data=data):
    data.ctrl[:] = np.zeros(model.nu)

def move(data=data):
    pos = data.qpos[:3] # [x, y, z, roll, pitch, yaw]
    data.qpos[0] += 0.0001

def control(data=data):
    data.qfrc_applied[:] = 0
    force = 3
    if keyboard.is_pressed('up'):
        data.qfrc_applied[0] = force  # Forward
    if keyboard.is_pressed('down'):
        data.qfrc_applied[0] = -force  # Backward
    if keyboard.is_pressed('left'):
        data.qfrc_applied[1] = force  # Left
    if keyboard.is_pressed('right'):
        data.qfrc_applied[1] = -force  # Right

    if not keyboard.is_pressed('up') and not keyboard.is_pressed('down'):
        data.qfrc_applied[0] = -data.qvel[0] * 5
    if not keyboard.is_pressed('left') and not keyboard.is_pressed('right'):
        data.qfrc_applied[1] = -data.qvel[1] * 5


# visualising
with mujoco.viewer.launch_passive(model, data) as viewer:
    while True:
        try:
            reset()
            control()
            mujoco.mj_step(model, data)
            viewer.sync()

        except KeyboardInterrupt:
            break

