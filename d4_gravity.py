import numpy as np
import mujoco, mujoco.viewer
import time, keyboard


model = mujoco.MjModel.from_xml_path("xmls/env.xml")
data = mujoco.MjData(model)


gravVal = 9.81
def GravControl():
    global gravVal
    if keyboard.is_pressed('up'):
        gravVal += 1
        model.opt.gravity[2] = -gravVal
        print(f"grav increased {gravVal} m/s^2")
    elif keyboard.is_pressed('down'):
        gravVal -= 1
        model.opt.gravity[2] = -gravVal     # gravity (x0, y1, z2) direction
        print(f"grav decreased {gravVal} m/s^2")


if __name__ == "__main__":
    # visualising
    with mujoco.viewer.launch_passive(model, data) as viewer:
        start_time = time.time()
        while viewer.is_running():
            try:
                
                GravControl()
                mujoco.mj_step(model, data)
                viewer.sync()
                time.sleep(0.02)

            except KeyboardInterrupt:
                break