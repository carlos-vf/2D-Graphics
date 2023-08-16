# -*- coding: utf-8 -*-
"""

@author: Carlos Velázquez Fernández

Gráficos por Computador
    Práctica 4  

"""

import tkinter as tk
import numpy as np
import math
import random

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# Colors
global COLOR
COLOR = '#000000'
BUTTON_COLOR = '#C0C0C0'
ACTIVE_BUTTON_COLOR = '#A0A0A0'


################################## FUNCTIONS #################################

# Deletes all objects from canvas    
def clearCanvas():
    canvas.delete("all")
     

# Transforms the coordinates from (right-left, up-down) to cartesian
def toCartesian(x, y):
    newX = int(x - CANVAS_WIDTH/2)
    newY = int(CANVAS_HEIGHT/2 - y)
    return newX, newY


def toUpDown(x, y):
    newX = x + CANVAS_WIDTH/2
    newY = (-1) * (y - CANVAS_HEIGHT/2)
    return newX, newY
    

# Changes the color of the element
def chooseColor():
    global COLOR
    colorCode = tk.colorchooser.askcolor(title ="Choose color")
    COLOR = colorCode[1]


# Initializes the korch curves function
def initKorchCurves():
    
    n = 2
    alpha = 90
    axiom = "F-F-F-F"
    rules = [["F","F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([-100, -100])
    zoom = 5
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)


# Initializes the Sierpisnki Gasket function  
def initSierpisnkiGasket():
    
    n = 6
    alpha = 60
    axiom = "R"
    rules = [["L", "R+L+R"],
             ["R", "L-R-L"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([-250, -200])
    zoom = 8
    direction = 0
    drawLSystem(text, origin, alpha, direction, zoom)
    

# Initializes the Islands and Lakes Gasket function      
def initIslands():
    
    n = 2
    alpha = 90
    axiom = "F+F+F+F"
    rules = [["F", "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF"],
             ["f", "ffffff"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([100, -100])
    zoom = 5
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)
    
    
    
# Initializes a plant function
def initPlant1():
    
    n = 5
    alpha = 22.5
    axiom = "X"
    rules = [["F", "FF"],
             ["X", "F-[[X]+X]+F[+FX]-X"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -200])
    zoom = 5
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)
    

# Initializes a plant function
def initPlant2():
    
    n = 7
    alpha = 25.7
    axiom = "X"
    rules = [["F", "FF"],
             ["X", "F[+X][-X]FX"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -250])
    zoom = 2
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)
    

# Initializes a plant function    
def initPlant3():
    
    n = 5
    alpha = 20
    axiom = "F"
    rules = [["F", "F[+F]F[-F][F]"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -250])
    zoom = 8
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)
    

# Initializes a plant function    
def initPlant4():
    
    n = 5
    alpha = 20
    axiom = "F"
    rules = [["F", "F[+F]F[-F][F]"],
             ["F", "F[+F]F"],
             ["F", "F[-F]F"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -250])
    zoom = 8
    direction = 90
    drawLSystem(text, origin, alpha, direction, zoom)
    

# Creates a sentence given an axiom and a set of rules
# n: number of generations
# axiom: original axiom
# rules: a list of rules [[A, AB], ...[...]]    
def generateLSystem(n, axiom, rules):
    
    lastText = axiom
    constant = True

    for i in range(n):
        newText = ""
        for char in lastText:
            possibleRules = []
            for rule in rules:
                if(rule[0] == char):
                    constant = False
                    possibleRules.append(rule[1])
   
            if (constant):
                newText = newText + char
            else:
                ruleToApply = random.choice(possibleRules)  
                newText = newText + ruleToApply
            constant = True
            
        lastText = newText
        
    return lastText
        

# Creates a sentence given an axiom and a set of rules
# text: sentence composed by F, L, R, +, -, [ or ] characters
# origin: point of origin
# alpha: angle for each rotation
# direction: initial direction (right=0, up=90, left=180, down=270)
# zoom: distance for each step
def drawLSystem(text, origin, alpha, direction, zoom):
    
    clearCanvas()
    
    currentPos = origin
    newPos = origin
    
    directionRad = math.radians(direction)
    alphaRad = math.radians(alpha)

    states = []
    directions = []

    for char in text:
        
        if char == "-":
            directionRad = directionRad - alphaRad
  
        elif char == "+":
            directionRad = directionRad + alphaRad
        
        elif char == "[":
            states.append(currentPos)
            directions.append(directionRad)
            
        elif char == "]":
            currentPos = states.pop()
            directionRad = directions.pop()
            
        elif char == "F" or char == "L"  or char == "R":
            newPos = [currentPos[0]+zoom*math.cos(directionRad), currentPos[1]+zoom*math.sin(directionRad)]
            
            x1, y1 = toUpDown(currentPos[0], currentPos[1])
            x2, y2 = toUpDown(newPos[0], newPos[1])
            canvas.create_line(x1, y1, x2, y2)
            
            currentPos = newPos
            
        elif char == "f":
            newPos = [currentPos[0]+zoom*math.cos(directionRad), currentPos[1]+zoom*math.sin(directionRad)]
            currentPos = newPos
            
        
            
    
################################## WINDOW ###################################
# Create Window
window = tk.Tk()
window.geometry("900x700")
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
canvas = tk.Canvas(window, width = CANVAS_WIDTH,  height = CANVAS_HEIGHT, bg = "white")
canvas.place(x=40, y=60)


################################### BUTTONS #################################
# Korch curves
korchCurvesButton = tk.Button(window, width = 20, text = "Korch Curves", command = initKorchCurves, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
korchCurvesButton.place(x=700, y=80) 

# Sierpinski Gasket
sierpinskiButton = tk.Button(window, width = 20, text = "Sierpinski Gasket", command = initSierpisnkiGasket, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
sierpinskiButton.place(x=700, y=120) 

# Islands
islandsButton = tk.Button(window, width = 20, text = "Islands", command = initIslands, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
islandsButton.place(x=700, y=160) 

# Plant 1
plant1Button = tk.Button(window, width = 20, text = "Plant 1", command = initPlant1, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
plant1Button.place(x=700, y=200)

# Plant 2
plant2Button = tk.Button(window, width = 20, text = "Plant 2", command = initPlant2, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
plant2Button.place(x=700, y=240)  

# Plant 3
plant3Button = tk.Button(window, width = 20, text = "Plant 3", command = initPlant3, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
plant3Button.place(x=700, y=280)  

# Plant 4
plant4Button = tk.Button(window, width = 20, text = "Plant 4\n(Stochastic)", command = initPlant4, background=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
plant4Button.place(x=700, y=320) 


################################### LABELS #################################
# Fractals
fractalsLbl = tk.Label(window, text = "L-Systems", font=("Arial", 18))
fractalsLbl.place(x=270, y=15)


################################# INTERACTIONS ###############################
canvas.focus_set()


window.mainloop()
