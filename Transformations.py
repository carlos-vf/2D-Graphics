# -*- coding: utf-8 -*-
"""

@author: Carlos Velázquez Fernández

Gráficos por Computador
    Práctica 2
    
@version: 12.0    

"""

import tkinter as tk
from tkinter import ttk
import math
import numpy as np

canvasWidth = 700
canvasHeight = 500

# Buffers
linePoints = []        # linePoints = [[x1, y1], [x2, y2]]
pointsBuffer = []       # pointsBuffer = [[x1, y1], ..., [xn, yn]]
figuresBuffer = []      # figuresBuffer = [m0, ..., mn]

# Colors
global COLOR
COLOR = '#000000'
BUTTON_COLOR = '#C0C0C0'
ACTIVE_BUTTON_COLOR = '#A0A0A0'

# Modes
NONE = 0
DOT = 1
LINE = 2
FIGURE = 3

# Radio Buttons
RB_STATE = 0

global DRAWING_MODE
DRAWING_MODE = NONE

newFigure = True


################################## FUNCTIONS #################################

# Draws an object according to the selected mode
def draw(event):
    
    global figuresBuffer
    global newFigure
    
    canvas.focus_set()

    
    if (DRAWING_MODE == DOT):
        canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
        x, y = toCartesian(event.x, event.y)
        pointListRepresentation([[x, y]])
    
    
    if (DRAWING_MODE == LINE):
        
        if (comboLine.get() == "Line Slope Intercept 1"):
            linePoints.append(toCartesian(event.x, event.y))
            canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
            if (len(linePoints) == 2):
                x1, y1 = linePoints[0]
                x2, y2 = linePoints[1]
                pointsBuffer = createLineSlopeInterceptFirstOctant(x1, y1, x2, y2)
                pointListRepresentation(pointsBuffer)
                linePoints.clear()
        
        
        if (comboLine.get() == "Line Slope Intercept 2"):
            linePoints.append(toCartesian(event.x, event.y))
            canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
            if (len(linePoints) == 2):
                x1, y1 = linePoints[0]
                x2, y2 = linePoints[1]
                pointsBuffer = createLineSlopeInterceptAllCases(x1, y1, x2, y2)
                pointListRepresentation(pointsBuffer)
                linePoints.clear()
                
                
        if (comboLine.get() == "DDA"):
            linePoints.append(toCartesian(event.x, event.y))
            canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
            if (len(linePoints) == 2):
                x1, y1 = linePoints[0]
                x2, y2 = linePoints[1]
                pointsBuffer = createLineDDA(x1, y1, x2, y2)
                pointListRepresentation(pointsBuffer)
                linePoints.clear()
                
                
        if (comboLine.get() == "Bresenham"):
            linePoints.append(toCartesian(event.x, event.y))
            canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
            if (len(linePoints) == 2):
                x1, y1 = linePoints[0]
                x2, y2 = linePoints[1]
                pointsBuffer = createLineBresenham(x1, y1, x2, y2)
                pointListRepresentation(pointsBuffer)
                linePoints.clear()
            
            
    if (DRAWING_MODE == FIGURE):
        pressEnter.place(x=53, y=580)
        newCoordinates = toCartesian(event.x, event.y)
        linePoints.append(newCoordinates)   # Update line buffer
        homogeneousCoord = np.array([[newCoordinates[0]], [newCoordinates[1]], [1]])
        if (newFigure):
            figuresBuffer.append(np.matrix(homogeneousCoord))
            newFigure = False
        else:
            figuresBuffer[-1] = np.concatenate([figuresBuffer[-1], homogeneousCoord], axis=1)    # Update figure buffer
        canvas.create_rectangle((event.x, event.y) * 2, outline = COLOR, fill= COLOR)
        if (len(linePoints) == 2):
            x1, y1 = linePoints[0]  # Update line buffer
            x2, y2 = linePoints[1]
            createLineBresenham(x1, y1, x2, y2) # Draw line
            linePoints.clear()
            linePoints.append([x2, y2])
        vertexListRepresentation(figuresBuffer[-1]) # Show vertices
  
    
# Draws a line following the Slope Intercept algorithm for the first octant
# x1, y1: origin point
# x2, y2: ending point
def createLineSlopeInterceptFirstOctant(x1, y1, x2, y2):
    
    # If lines goes from right to left, then swap
    if (x2 < x1):
        tempX, tempY = x1, y1
        x1, y1 = x2, y2
        x2, y2 = tempX, tempY

    x, y = x1, y1               # Initial points
    L = []                      # List of points to be drawn
    
    dx, dy= x2- x1, y2 - y1     # Distance
    m = dy / dx                 # Slope    
    b = y1 - m * x1             # Height of the line in the origin

    while (x <= x2):            # Calculate points
        L.append([x, y])
        x += 1
        y = round(m * x + b)
    
    for point in L:             # Draw the points
        canvas.create_rectangle(toUpDown(point[0], point[1]) * 2, outline = COLOR, fill= COLOR)

    return L

# Draws a line following the Slope Intercept algorithm for all cases
# x1, y1: origin point
# x2, y2: ending point
def createLineSlopeInterceptAllCases(x1, y1, x2, y2):
    
    # If lines goes from right to left, then swap
    if (x2 < x1):
        tempX, tempY = x1, y1
        x1, y1 = x2, y2
        x2, y2 = tempX, tempY

    x, y = x1, y1               # Initial points
    L = []                      # List of points to be drawn
    
    
    # m = inf
    if (x1 == x2):
        while(y != y2):
            L.append([x, y])
            y += 1
    
    # m != inf        
    else:
        
        dx, dy= x2- x1, y2 - y1     # Distance
        m = dy / dx             # Slope
        b = y1 - m * x1
    
        # Displacement in y
        if (m > 1 or m < -1):                 # If slope greater than 45º, then swap and recalculate
            m = 1 / m
            b = x1 - m * y1         
            
            x, y = y, x                     # Swap
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            
            if (x1 > x2):
                 while (x > x2):            # Calculate points
                    L.append([y, x])   
                    x -= 1
                    y = round(m * x + b)
            else:
                while (x < x2):            # Calculate points
                    L.append([y, x])     
                    x += 1
                    y = round(m * x + b)
           
        # Displacement in x
        else:
            while (x < x2):
                L.append([x, y])
                x += 1
                y = round(m * x + b)
                    
      
    for point in L:             # Draw the points
        canvas.create_rectangle(toUpDown(point[0], point[1]) * 2, outline = COLOR, fill= COLOR)    
        
    return L

# Draws a line following the DDA algorithm
# x1, y1: origin point
# x2, y2: ending point
def createLineDDA(x1, y1, x2, y2):
    
    L = []                      # List of points to be draw
    dx, dy= x2- x1, y2 - y1     # Distance
    
    if (abs(dx) >= abs(dy)):
        m = abs(dx)
    else:
        m = abs(dy)
    
    dx_p = dx / m
    dy_p = dy / m
    
    x = x1 + 0.5
    y = y1 + 0.5
    
    i = 0           # Para más de una línea: i = 1
    
    while (i <= m):
        x = x + dx_p
        y = y + dy_p
        L.append([math.floor(x), math.floor(y)])
        i += 1
    
    for point in L:             # Draw the points
        canvas.create_rectangle(toUpDown(point[0], point[1]) * 2, outline = COLOR, fill= COLOR)    

    return L


def bresenhamLineLow(x1, y1, x2, y2):
    L = []
    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    
    if dy < 0:
        yi = -1
        dy = -dy
    
    ne = (2 * dy) - dx
    x, y = x1, y1

    while (x < x2):
        L.append([x, y])
        if ne > 0:
            y += yi
            ne += (2 * (dy - dx))
        else:
            ne += 2*dy
        x += 1
    return L


def bresenhamLineHigh(x1, y1, x2, y2):
    L = []
    dx = x2 - x1
    dy = y2 - y1
    xi = 1
    
    if dx < 0:
        xi = -1
        dx = -dx
        
    ne = (2 * dx) - dy
    x, y = x1, y1

    while (y < y2):
        L.append([x, y])
        if ne > 0:
            x += xi
            ne += (2 * (dx - dy))
        else:
            ne += 2*dx
        y += 1
    return L
    

# Draws a line following the Bresenham algorithm
# x1, y1: origin point
# x2, y2: ending point
def createLineBresenham(x1, y1, x2, y2):
    
    # Greater displacement in X
    if abs(y2 - y1) < abs(x2 - x1):
        if x1 > x2:
            tempX, tempY = x1, y1
            x1, y1 = x2, y2
            x2, y2 = tempX, tempY
        L = bresenhamLineLow(x1, y1, x2, y2)
   
    # Greater displacement in Y 
    else:
        if y1 > y2:
            tempX, tempY = x1, y1
            x1, y1 = x2, y2
            x2, y2 = tempX, tempY
        L = bresenhamLineHigh(x1, y1, x2, y2)

    for point in L:             # Draw the points
        canvas.create_rectangle(toUpDown(point[0], point[1]) * 2, outline = COLOR, fill= COLOR)    

    return L

# Change between drawing modes
def changeMode(newMode):
    global DRAWING_MODE
    DRAWING_MODE = newMode
       

# Deletes all objects from canvas    
def clearCanvas():
    canvas.delete("all")
    canvas.create_line(0, canvasHeight/2, canvasWidth, canvasHeight/2, fill = "red")
    canvas.create_line(canvasWidth/2, 0, canvasWidth/2, canvasHeight, fill = "red")
    canvas.create_line(2, 2, canvasWidth, 2, fill = "black")
    canvas.create_line(2, 2, 2, canvasHeight, fill = "black")
    canvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight, fill = "black")
    canvas.create_line(2, canvasHeight, canvasWidth, canvasHeight, fill = "black")
   
    linePoints.clear()
    
    clearFields()
    
# Deletes all objects from canvas and the info  
def clearCanvasAndText():
    canvas.delete("all")
    canvas.create_line(0, canvasHeight/2, canvasWidth, canvasHeight/2, fill = "red")
    canvas.create_line(canvasWidth/2, 0, canvasWidth/2, canvasHeight, fill = "red")
    canvas.create_line(2, 2, canvasWidth, 2, fill = "black")
    canvas.create_line(2, 2, 2, canvasHeight, fill = "black")
    canvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight, fill = "black")
    canvas.create_line(2, canvasHeight, canvasWidth, canvasHeight, fill = "black")
   
    linePoints.clear()
    log.delete(0,tk.END)
    
    global figuresBuffer
    figuresBuffer = [[]]
    
    clearFields()
    
    
# Clears the data from all text fields
def clearFields():
    
    translationX.delete('1.0', "end")
    translationY.delete('1.0', "end")
    
    scalingX.delete('1.0', "end")
    scalingY.delete('1.0', "end")
    
    rotationAlpha.delete('1.0', "end")
    
    shearX.delete('1.0', "end")
    shearY.delete('1.0', "end")
    
    reflectionNone.select()
    reflectionM.delete('1.0', "end")
    reflectionB.delete('1.0', "end")
    

# Updates de tag with the mouse coordinates        
def motion(event):
    x, y = event.x, event.y
    x, y = toCartesian(x, y)
    mouseCoordinates.config(text="X: " + str(round(x)) + ", Y: " + str(round(y)))


# Transforms the coordinates from (right-left, up-down) to cartesian
def toCartesian(x, y):
    newX = int(x - canvasWidth/2)
    newY = int(canvasHeight/2 - y)
    return newX, newY


def toUpDown(x, y):
    newX = x + canvasWidth/2
    newY = (-1) * (y - canvasHeight/2)
    return newX, newY
    

# Changes the color of the element
def chooseColor():
    global COLOR
    colorCode = tk.colorchooser.askcolor(title ="Choose color")
    COLOR = colorCode[1]


def listToString(listOfPoints):
    newList = "List of Points:\n"
    for point in listOfPoints:
        newList += "(" + str(point[0]) + ", " + str(point[1]) + ")\n"
    return newList
    

def pointListRepresentation(pointsBuffer):
    log.delete(0,tk.END)
    log.insert(0, "List of Points")
    log.insert(1, "")
    for i in range (2, len(pointsBuffer) + 2):
        log.insert(i, str(pointsBuffer[i-2]))
        
        
def vertexListRepresentation(verticesBuffer):
    log.delete(0,tk.END)
    log.insert(0, "List of Vertices")
    log.insert(1, "")
    shape = np.shape(verticesBuffer)
    for i in range (shape[1]):
        point = verticesBuffer[:, i]
        x = int(point[0])
        y = int(point[1])
        log.insert(tk.END, "( " + str(x) + ", " + str(y) + " )")

                
def addNewFigure():
    global newFigure
    newFigure = True
    
    linePoints.clear()
    pressEnter.place_forget()
   
    
# Apply transformations to the figures
def transform():
    
    log.delete(0,tk.END)
    
    # Get values for each transformation
    values = getTransformationValues()
    translation = values[0]
    scaling = values[1]
    rotation = values[2]
    shear = values[3]
    reflection = values[4]
    
    
    # Translation
    translationMatrix = np.matrix([[1, 0, translation[0]], 
                                   [0, 1, translation[1]], 
                                   [0, 0, 1]]).astype('int32')
    if ((translation[0] != 0) or (translation[1] != 0)):
        log.insert(tk.END, "Translation completed.")
        log.insert(tk.END, "X = " + str(translation[0]) + "; Y = " + str(translation[1]))  
        log.insert(tk.END, " ")
       
        
    # Scaling
    if (scaling[0] == 0):
        scaling[0] = 1
    if (scaling[1] == 0):
            scaling[1] = 1
    scalingMatrix = np.matrix([[scaling[0], 0, 0], 
                               [0, scaling[1], 0], 
                               [0, 0, 1]]).astype('float64')
    if ((scaling[0] != 1) or (scaling[1] != 1)):
        log.insert(tk.END, "Scaling completed.")
        log.insert(tk.END, "X = " + str(scaling[0]) + "; Y = " + str(scaling[1]))  
        log.insert(tk.END, " ")
    
    
    # Rotation
    alpha = rotation[0]
    clock = rotation[1]
    if (clock == "Anticlockwise"):
        alpha = -alpha
    alphaRad = math.radians(alpha)
    rotationMatrix = np.matrix([[math.cos(alphaRad),-math.sin(alphaRad), 0], 
                                [math.sin(alphaRad), math.cos(alphaRad), 0],
                                [0, 0, 1]]).astype('float64')
    if (rotation[0] != 0):
        log.insert(tk.END, "Rotation completed.")
        log.insert(tk.END, "Alpha = " + str(abs(alpha)) + "º; " + str(clock))  
        log.insert(tk.END, " ")
        
    
    # Shear
    shearMatrix = np.matrix([[1, shear[0], 0], 
                             [shear[1], 1, 0], 
                             [0, 0, 1]]).astype('float64')
    if ((shear[0] != 0) or (shear[1] != 0)):
        log.insert(tk.END, "Shear completed.")
        log.insert(tk.END, "X = " + str(shear[0]) + "; Y = " + str(shear[1]))  
        log.insert(tk.END, " ")
        
        
         
    # Reflection
    m, b = reflection[1], reflection[2]
    if (reflection[0] == 0):
        reflectionMatrix = np.matrix([[1, 0, 0], 
                                      [0, 1, 0], 
                                      [0, 0, 1]]).astype('float64')
    elif (reflection[0] == 1):     # X axis
        reflectionMatrix = np.matrix([[1, 0, 0], 
                                      [0, -1, 0], 
                                      [0, 0, 1]]).astype('float64')
        log.insert(tk.END, "Reflection over X axis completed.")
        log.insert(tk.END, " ")
    elif (reflection[0] == 2):   # Y axis
        reflectionMatrix = np.matrix([[-1, 0, 0], 
                                      [0, 1, 0], 
                                      [0, 0, 1]]).astype('float64')
        log.insert(tk.END, "Reflection over Y axis completed.")
        log.insert(tk.END, " ")
    else:                        # New axis
        reflectionMatrix = np.matrix([[1-m*m, 2*m,  -2*m*b], 
                                      [ 2*m, m*m-1,   2*b ], 
                                      [  0,    0,      1  ]]).astype('float64')
        reflectionMatrix = (1/(1+m*m)) * reflectionMatrix
        log.insert(tk.END, "Reflection over line 'y = " + str(m) + "x + " + str(b) + "' completed.")
        log.insert(tk.END, " ")
        
    
    # Calculate final matrix
    finalMatrix = np.matmul(translationMatrix, scalingMatrix)   # TrSc = Tr * Sc
    finalMatrix = np.matmul(finalMatrix, rotationMatrix)        # TrScRt = TrSc * Rt
    finalMatrix = np.matmul(finalMatrix, shearMatrix)           # TrScRtSh = TrScRt * Sh
    finalMatrix = np.matmul(finalMatrix, reflectionMatrix)      # TrScRtShRe = TrScRtSh * Re
    
    '''
    # Apply all transformations to all figures
    newFigures = []
    global figuresBuffer
    for fig in figuresBuffer:
        newFig = np.matmul(finalMatrix, fig)
        newFigures.append(newFig)
    figuresBuffer = newFigures
    redrawFigures()
    '''
    
    # Apply all transformations to last figure
    global figuresBuffer
    newFig = np.matmul(finalMatrix, figuresBuffer[-1])
    figuresBuffer[-1] = newFig
    redrawFigures()
    
    print(figuresBuffer[-1])
    
    


# Returns a list with all the values from the text fields
# [[Translation], [scaling], [rotation], [shear], [reflection]]
def getTransformationValues():
    
    tx = translationX.get("1.0","end-1c")
    ty = translationY.get("1.0","end-1c")
    
    scx = scalingX.get("1.0","end-1c")
    scy = scalingY.get("1.0","end-1c")
    
    rAlpha = rotationAlpha.get("1.0","end-1c")
    rClock = rotationClock.get()
    
    shx = shearX.get("1.0","end-1c")
    shy = shearY.get("1.0","end-1c")
    
    rfButton = str(reflectionOption.get())
    rfM = reflectionM.get("1.0","end-1c")
    rfB = reflectionB.get("1.0","end-1c")
    
    values = [[tx, ty], [scx, scy], [rAlpha, rClock], [shx, shy], [rfButton, rfM, rfB]]
    
    for i in range(len(values)):
        for j in range(len(values[i])):
            if (values[i][j].lstrip("-").isdigit()):
                values[i][j] = int(values[i][j])
            if (values[i][j] == ""):
                values[i][j] = 0
                   
    return values


# Redraws all figures of canvas
def redrawFigures():
    clearCanvas()
    for fig in figuresBuffer:
        shape = np.shape(fig)
        for i in range(shape[1] - 1):
            point1 = fig[:, i]
            point2 = fig[:, i+1]
            createLineBresenham(int(point1[0]), int(point1[1]), int(point2[0]), int(point2[1]))
    

    
################################## WINDOW ###################################
# Create Window
window = tk.Tk()
window.geometry("1400x700")
window.title("Graficos por Computador")


# Configure window
window.columnconfigure(0, weight=3)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
for i in range(10):
    window.rowconfigure(i, weight=1)



################################### CANVAS ##################################
# Create canvas
canvas = tk.Canvas(window, width = canvasWidth,  height = canvasHeight, bg = "white")
canvas.grid(column=0, row=0, columnspan=6, rowspan=8, sticky=tk.W, padx = 50, pady = 50)


# Divide canvas
canvas.create_line(0, canvasHeight/2, canvasWidth, canvasHeight/2, fill = "red")
canvas.create_line(canvasWidth/2, 0, canvasWidth/2, canvasHeight, fill = "red")

# Borders
canvas.create_line(2, 2, canvasWidth, 2, fill = "black")
canvas.create_line(2, 2, 2, canvasHeight, fill = "black")
canvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight, fill = "black")
canvas.create_line(2, canvasHeight, canvasWidth, canvasHeight, fill = "black")

# List of points canvas
cpoints = tk.Canvas(window, width = 290,  height = 500, bg = "white")
cpoints.place(x=1070, y=60)



################################### BUTTONS #################################
# Clear
clear = tk.Button(window, width = 80, text = "Clear", command = clearCanvasAndText, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
clear.grid(column=0, row=8, sticky=tk.W, padx = 115, pady = 25)

# Mouse
drawNone = tk.Button(window, width = 20, text = "Mouse", command = lambda: changeMode(NONE), background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
drawNone.place(x=800, y=60) 

# Dot
drawDot = tk.Button(window, width = 20, text = "Point", command = lambda: changeMode(DOT), background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
drawDot.place(x=800, y=100) 

# Line
drawLine = tk.Button(window, width = 20, text = "Line", command = lambda: changeMode(LINE), background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
drawLine.place(x=800, y=140)

# Figure
drawFigure = tk.Button(window, width = 20, text = "Figure", command = lambda: changeMode(FIGURE), background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
drawFigure.place(x=800, y=210) 

# Choose color
chooseColor = tk.Button(window, height = 33, width = 5, text = "C\n\nO\n\nL\n\nO\n\nR", command = chooseColor, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
chooseColor.place(x=990, y=60) 

# Apply transformations
apply = tk.Button(window, width = 20, text = "Apply", command = lambda: transform(), background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
apply.place(x=800, y=590) 


################################### LABELS #################################
# Mouse Coordinates
mouseCoordinates = tk.Label(window, text = "0, 0", bg='white')
mouseCoordinates.place(x=660, y=70)

# Translation
translation = tk.Label(window, text = "Translation")
translation.place(x=840, y=250)
translationXlbl = tk.Label(window, text = "X :")
translationXlbl.place(x=800, y=275)
translationYlbl = tk.Label(window, text = "Y :")
translationYlbl.place(x=880, y=275)

# Scalation
scaling = tk.Label(window, text = "Scaling")
scaling.place(x=850, y=310)
scalingXlbl = tk.Label(window, text = "X :")
scalingXlbl.place(x=800, y=335)
scalingYlbl = tk.Label(window, text = "Y :")
scalingYlbl.place(x=880, y=335)

# Rotation
rotation = tk.Label(window, text = "Rotation")
rotation.place(x=850, y=370)
rotationAlphalbl = tk.Label(window, text = "Alpha :")
rotationAlphalbl.place(x=775, y=395)

# Shear
shear = tk.Label(window, text = "Shearing")
shear.place(x=850, y=430)
shearXlbl = tk.Label(window, text = "X :")
shearXlbl.place(x=800, y=455)
shearYlbl = tk.Label(window, text = "Y :")
shearYlbl.place(x=880, y=455)

# Reflection
reflection = tk.Label(window, text = "Reflection")
reflection.place(x=850, y=490)
relfexionNewlbl = tk.Label(window, text = "y  =            *  x  +          ")
relfexionNewlbl.place(x=810, y=540)

# Press enter
pressEnter = tk.Label(window, text = "Press 'enter' to save the figure.")


################################### LISTBOXES #################################
# Points
log = tk.Listbox(window, width = 48, height = 31)
log.place(x=1070, y=60)


################################### COMBOBOXES #################################
# Type of line
comboLine = ttk.Combobox(state="readonly", width=21,
                         values=["Line Slope Intercept 1",
                                "Line Slope Intercept 2", "DDA", "Bresenham"])
comboLine.set("Bresenham")
comboLine.place(x=800, y=170)

# Rotation
rotationClock = ttk.Combobox(state="readonly", width=12,
                         values=["Clockwise", "Anticlockwise"])
rotationClock.set("Clockwise")
rotationClock.place(x=880, y=395)


################################### TEXT FIELDS #################################
# Translation
translationX = tk.Text(window, height=1, width=5)
translationX.place(x=820, y=275)
translationY = tk.Text(window, height=1, width=5)
translationY.place(x=900, y=275)

# Scaling
scalingX = tk.Text(window, height=1, width=5)
scalingX.place(x=820, y=335)
scalingY = tk.Text(window, height=1, width=5)
scalingY.place(x=900, y=335)

# Rotation
rotationAlpha = tk.Text(window, height=1, width=5)
rotationAlpha.place(x=820, y=395)

# Shear
shearX = tk.Text(window, height=1, width=5)
shearX.place(x=820, y=455)
shearY = tk.Text(window, height=1, width=5)
shearY.place(x=900, y=455)

# Relexion
reflectionM = tk.Text(window, height=1, width=3)
reflectionM.place(x=835, y=540)
reflectionB = tk.Text(window, height=1, width=3)
reflectionB.place(x=910, y=540)


################################### RADIO BUTTONS #################################
# reflection
reflectionOption = tk.IntVar()
reflectionNone = tk.Radiobutton(window, text="None", variable=reflectionOption, value=0)
reflectionNone.place(x=790, y=515)
reflectionX = tk.Radiobutton(window, text="X", variable=reflectionOption, value=1)
reflectionX.place(x=850, y=515)
reflectionY = tk.Radiobutton(window, text="Y", variable=reflectionOption, value=2)
reflectionY.place(x=890, y=515)
reflectionNew = tk.Radiobutton(window, text="New", variable=reflectionOption, value=3)
reflectionNew.place(x=930, y=515)
reflectionNone.select()


################################# INTERACTIONS ###############################
canvas.focus_set()
canvas.bind("<Button-1>", draw)
canvas.bind('<Motion>', motion)
canvas.bind('<Return>', lambda event: addNewFigure())


window.mainloop()
