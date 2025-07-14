import numpy as np
import mujoco, mujoco.viewer
import time, keyboard


model = mujoco.MjModel.from_xml_path("xmls/env.xml")
data = mujoco.MjData(model)



def forceControl():
    force = np.zeros(6)
    force[:] = 0
    if keyboard.is_pressed('right'):
        force[0] = 10.0
    elif keyboard.is_pressed('left'):
        force[0] = -10.0
    elif keyboard.is_pressed('up'):
        force[1] = 10.0
    elif keyboard.is_pressed('down'):
        force[1] = -10.0
    
    return force


if __name__ == "__main__":
    # visualising
    with mujoco.viewer.launch_passive(model, data) as viewer:
        start_time = time.time()
        while viewer.is_running():
            data.xfrc_applied[:] = 0
            try:   
                
                force = forceControl()
                sphereID = model.body('sphere').id
                data.xfrc_applied[sphereID] = force
                
                mujoco.mj_step(model, data)
                viewer.sync()
                time.sleep(0.02)

            except KeyboardInterrupt:
                break