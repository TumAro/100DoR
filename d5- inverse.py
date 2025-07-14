import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from math import sqrt

# ------------ inverse kinematics math ---------------------

'''
c1 = (x1,y1)
c2 = (x2,y2)
'''
def intersection(c1,r1, c2,r2):
    x1, y1 = c1
    x2, y2 = c2
    
    # Calculate distance between centers
    dx = x2 - x1
    dy = y2 - y1
    D = sqrt(dx**2 + dy**2)
    
   # Check valid intersection conditions
    if D > (r1 + r2) or D < abs(r1 - r2) or D == 0:
        # Return projection along the line if no intersection
        ratio = r1 / (r1 + r2) if (r1 + r2) != 0 else 0
        return (x1 + ratio*dx, y1 + ratio*dy)
    
    # Calculate intersection point (using standard geometric formula)
    a = (r1**2 - r2**2 + D**2) / (2 * D)
    h = sqrt(r1**2 - a**2)
    
    # Midpoint between intersections
    xm = x1 + a*dx/D
    ym = y1 + a*dy/D

    # Calculate both intersection points
    x_upper = xm - h*dy/D
    y_upper = ym + h*dx/D
    
    x_lower = xm + h*dy/D
    y_lower = ym - h*dx/D


    if y_lower > y_upper:
        return (x_lower, y_lower)
    else:
        return (x_upper, y_upper)

def calculateJoints(lengths, A, E):
    joints  = [A]
    
    for i in range(1, len(lengths)):
        c1 = joints[i-1]
        c2 = E
        r1 = lengths[i-1]
        r2 = sum(lengths[i-1:])
    
        jNew = intersection(c1,r1,c2,r2)
        print(f"{c1} -> {jNew}")
        joints.append(jNew)
    
    joints.append(E)
    return joints

def calculateAngles(lengths, joints):
    angles = []
    for i in range(1,len(lengths)):
        vec = np.asarray(joints[i]) - np.asarray(joints[i-1])
        theta = np.arctan2(vec[1], vec[0])
        angles.append(theta)
    return angles

def validateJoints(joints, min_angle=-np.pi/4, max_angle=np.pi/4):
    """Check if the joint configuration is valid based on angle constraints"""
    angles = calculateAngles(arm_lengths, joints)
    
    # Check relative angles between segments
    for i in range(1, len(angles)):
        relative_angle = angles[i] - angles[i-1]
        # Normalize angle to [-pi, pi]
        while relative_angle > np.pi: relative_angle -= 2*np.pi
        while relative_angle < -np.pi: relative_angle += 2*np.pi
        
        if relative_angle < min_angle or relative_angle > max_angle:
            return False
    return True

# ----------------------------------------------------------

# Set up the robot arm parameters
base = (0, 0)
arm_lengths = [3, 6,3, 5] # =======================> TWEAK THIS
max_range = sum(arm_lengths) + 2
current_pos = [3, 3]
target_pos = [3, 3]

# Create tkinter window
root = tk.Tk()
root.title("Inverse Kinematics")

# ===========================================================================
# setup the gui

# Create matplotlib figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.grid(True)
ax.set_aspect('equal')

# Initialize the line and dots for the arm
line, = ax.plot([], [], 'k-', lw=2)
dots, = ax.plot([], [], 'ro', ms=8)
target, = ax.plot([], [], 'bo', ms=10)

# Embed matplotlib figure in tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

# Function to update the plot with current arm position
def update_arm_display():
    joints = calculateJoints(arm_lengths, base, (current_pos[0], current_pos[1]))
    
    # Use the angles function to check if configuration is valid
    if not validateJoints(joints):
        print("Warning: Target position creates an invalid joint configuration")
    
    x_coords = [joint[0] for joint in joints]
    y_coords = [joint[1] for joint in joints]
    
    line.set_data(x_coords, y_coords)
    dots.set_data(x_coords, y_coords)
    target.set_data([target_pos[0]], [target_pos[1]])
    
    # Display the joint angles for reference
    angles = calculateAngles(arm_lengths, joints)
    angle_degrees = [round(angle * 180 / np.pi, 1) for angle in angles]
    print(f"Joint angles (degrees): {angle_degrees}")
    
    canvas.draw_idle()

# Function to update target position
def update_target(*args):
    global target_pos
    target_pos = [x_slider.get(), y_slider.get()]
    target.set_data([target_pos[0]], [target_pos[1]])
    canvas.draw_idle()

# Function for the GO button
def on_go_clicked():
    global current_pos
    current_pos[0] = target_pos[0]
    current_pos[1] = target_pos[1]
    update_arm_display()

# =====================================================================
# setting up tkinter buttons
# Create controls
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, columnspan=3)

ttk.Label(frame, text="Target X:").grid(row=0, column=0, sticky="w")
x_slider = ttk.Scale(frame, from_=-max_range, to=max_range, length=200, orient="horizontal", command=update_target)
x_slider.set(3)
x_slider.grid(row=0, column=1)

ttk.Label(frame, text="Target Y:").grid(row=1, column=0, sticky="w")
y_slider = ttk.Scale(frame, from_=-max_range, to=max_range, length=200, orient="horizontal", command=update_target)
y_slider.set(3)
y_slider.grid(row=1, column=1)

go_button = ttk.Button(frame, text="GO", command=on_go_clicked)
go_button.grid(row=2, column=1, pady=10)

# Initial setup
update_target()
update_arm_display()

root.mainloop()