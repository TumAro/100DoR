from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import *

# Initialize window
window = Tk()
window.title("Forward Kinematics")
window.geometry("600x700")
window.resizable(False, False)

# Create frames
plotDiv = Frame(window)
plotDiv.pack(fill=BOTH, expand=True)
sliderDiv = Frame(window)
sliderDiv.pack(fill=X, padx=20, pady=20)

# Setup plot
fig = Figure(figsize=(6, 4), dpi=100)
plot = fig.add_subplot(111)
fig.tight_layout(pad=2.0)

# Set fixed plot properties
max_length = 10
plot.set_xlim(-max_length/2, max_length/2)
plot.set_ylim(0, max_length)
plot.grid(True)
plot.set_aspect('equal')

# Create canvas
canvas = FigureCanvasTkAgg(fig, master=plotDiv)
canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# Forward kinematics function --------------------------------------------
def forwardKinematics(a1, l1, a2, l2):
    o = (0, 0)
    midX = l1 * cos(a1)
    midY = l1 * sin(a1)
    endX = midX + l2 * cos(a1+a2)
    endY = midY + l2 * sin(a1+a2)
    return [o, (midX, midY), (endX, endY)]

# initialising the lines
line1, = plot.plot([0, 0], [0, 0], 'b-', linewidth=3)
line2, = plot.plot([0, 0], [0, 0], 'r-', linewidth=3)

# Update plot function
def updatePlot(event=None):
    a1 = a1Slider.get()
    l1 = l1Slider.get()
    a2 = a2Slider.get()
    l2 = l2Slider.get()
    
    o, mid, end = forwardKinematics(a1, l1, a2, l2)
    line1.set_data([o[0], mid[0]], [o[1], mid[1]])
    line2.set_data([mid[0], end[0]], [mid[1], end[1]])
    canvas.draw()

# Create sliders
a1Label = Label(sliderDiv, text="Angle 1")
a1Label.grid(row=0, column=0, padx=5, pady=5)
a1Slider = Scale(sliderDiv, from_=0, to=pi, resolution=0.01, orient=HORIZONTAL, length=400, command=updatePlot)
a1Slider.grid(row=0, column=1, padx=5, pady=5)

l1Label = Label(sliderDiv, text="Length 1")
l1Label.grid(row=1, column=0, padx=5, pady=5)
l1Slider = Scale(sliderDiv, from_=0.1, to=5.0, orient=HORIZONTAL, length=400, command=updatePlot)
l1Slider.grid(row=1, column=1, padx=5, pady=5)

a2Label = Label(sliderDiv, text="Angle 2")
a2Label.grid(row=2, column=0, padx=5, pady=5)
a2Slider = Scale(sliderDiv, from_=-pi, to=pi, resolution=0.01, orient=HORIZONTAL, length=400, command=updatePlot)
a2Slider.grid(row=2, column=1, padx=5, pady=5)

l2Label = Label(sliderDiv, text="Length 2")
l2Label.grid(row=3, column=0, padx=5, pady=5)
l2Slider = Scale(sliderDiv, from_=0.1, to=5.0, orient=HORIZONTAL, length=400, command=updatePlot)
l2Slider.grid(row=3, column=1, padx=5, pady=5)

# Initialize plot
a1Slider.set(0)
l1Slider.set(2.5)
a2Slider.set(0)
l2Slider.set(2.5)

window.mainloop()