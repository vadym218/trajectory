from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

app = Tk()
app.title('Freefall simulator')

# init input vars
xVel = 10
yVel = 0
height = 10
xVelStr = StringVar(value=xVel)
yVelStr = StringVar(value=yVel)
heightStr = StringVar(value=height)

# declare output vars
maxSpdStr = StringVar(value='Max speed: undefined')
flightTimeStr = StringVar(value='Flight time: undefined')
pathLenStr = StringVar(value='Path length: undefined')
xDistStr = StringVar(value='Horizotal distance: undefined')

# declare graphic
f = Figure()
g = f.add_subplot()
g.axis('equal')
g.set_frame_on(False)
g.tick_params(color='none')
canvas = FigureCanvasTkAgg(f, app)

# declare instant data vars
time = DoubleVar(value='0')
xStr = StringVar(value='X: 0 m')
yStr = StringVar(value='Y: 0 m')
spdStr = StringVar(value='Speed: 0 m/s')
instantData = LabelFrame(app, text='Instant Data')
instantDataContainer = Frame(instantData)
slider = Scale(instantDataContainer, from_=0, to=0, resolution=.05, variable=time, length=800, label='Time (s)', orient=HORIZONTAL)

# try parsing float
def parse_float(value):
    try:
        return float(value)
    except ValueError:
        return 0

# make calculations
flightTime = 0
def calculate(name, index, mode):
    global xVel, yVel, height, flightTime

    # get input
    xVel = parse_float(xVelStr.get())
    yVel = parse_float(yVelStr.get())
    height = abs(parse_float(heightStr.get()))

    # draw trajectory
    x = []
    y = []
    flightTime = ((yVel ** 2 + 19.6 * height) ** .5 + yVel) / 9.8
    for i in range(0, int(flightTime / .005) + 1):
        t = i * .005
        x.append(xVel * t)
        y.append(height + t * (yVel - 4.9 * t))
    g.clear()
    g.plot(x, y)
    g.axhline(0, color='lightgray')
    g.axvline(0, color='lightgray')
    canvas.draw()

    # calc output
    maxSpdStr.set('Max speed: ' + format(((yVel - 9.8 * flightTime) ** 2 + xVel ** 2) ** .5, ".2f") + ' m/s')
    flightTimeStr.set('Flight time: ' + format(flightTime, ".2f") + ' s')
    xDist = xVel * flightTime
    pathLenStr.set('Path length: ' + format((xVel ** 2 + (yVel - 9.8 * flightTime) ** 2) ** .5, ".2f") + ' m')
    xDistStr.set('Horizontal distance: ' + format(xDist, ".2f") + ' m')
    # yDist = 0
    # if yVel > 0:
    #     apogeeMoment = yVel / 9.8
    #     yDist = flightTime * (yVel + 4.9 * flightTime) - apogeeMoment * (yVel + 9.8 * apogeeMoment)
    # else: yDist = height

    # update slider
    slider.configure(to=flightTime)
calculate(None, None, None)

# recalculate on input change
xVelStr.trace(W, calculate)
yVelStr.trace(W, calculate)
heightStr.trace(W, calculate)

# update instant data
def update_instant(name, index, mode):
    t = min(flightTime, time.get())
    spdStr.set('Speed: ' + format(((yVel - 9.8 * t) ** 2 + xVel ** 2) ** .5, ".2f") + ' m/s')
    xStr.set('X: ' + format(xVel * t, ".2f") + ' m')
    yStr.set('Y: ' + format(height + t * (yVel - 4.9 * t), ".2f") + ' m')
update_instant(None, None, None)
time.trace(W, update_instant)

# validate input - only numbers are allowed
def is_valid(input):
    try:
        if input != '' and input != '-': float(input)
    except ValueError: return False
    else: return True
validator = app.register(is_valid)

# input form
input = LabelFrame(app, text='Input')

inputContainer = Frame(input)

Label(inputContainer, text='X velocity (m/s): ').pack(side='left')
Entry(
    inputContainer,
    textvariable=xVelStr,
    validate='key',
    validatecommand=(validator, '%P'),
    width=6
).pack(side='left')

Label(inputContainer, text=' Y velocity (m/s): ').pack(side='left')
Entry(
    inputContainer,
    textvariable=yVelStr,
    validate='key',
    validatecommand=(validator, '%P'),
    width=6
).pack(side='left')

Label(inputContainer, text=' Height (m): ').pack(side='left')
Entry(
    inputContainer,
    textvariable=heightStr,
    validate='key',
    validatecommand=(validator, '%P'),
    width=6
).pack(side='left')

inputContainer.pack(padx=(8, 14), pady=(6, 12))
input.grid(row=0, column=0, padx=8, pady=8, sticky='ew')

# output form
output = LabelFrame(app, text='Output')

outputContainer = Frame(output)

Label(outputContainer, textvariable=flightTimeStr).pack(side='left')
Label(outputContainer, textvariable=maxSpdStr).pack(side='left')
Label(outputContainer, textvariable=xDistStr).pack(side='left')
#Label(outputContainer, textvariable=pathLenStr).pack(side='left')

outputContainer.pack(padx=(8, 14), pady=(6, 12))
output.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

# trajctory form
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='ew')

# instant data form
slider.pack(side='left')

Label(instantDataContainer, textvariable=xStr).pack(side='left')
Label(instantDataContainer, textvariable=yStr).pack(side='left')
Label(instantDataContainer, textvariable=spdStr).pack(side='left')

instantDataContainer.pack(padx=(8, 14), pady=(6, 12))
instantData.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky='ew')

app.mainloop()
