import random
import sys
import time
import tkinter as tk
import numpy as np
import math

ke = 10000
m = 1

def move_to(x, y):
    canvas.coords(object_simulated,x-10,y-10,x+10,y+10)
    canvas.create_oval(x-0.5,y-0.5,x+0.5,y+0.5, fill ="black")
    root.update()
    return


root = tk.Tk()                                  # spawns the window (which will be called "root")
root.title("Simulation of Equation received")
canvas = tk.Canvas(root, width=1300, height=740) # creates a canvas to draw on
canvas.pack()                                   # spawns the squares and pack them in the canvas

object_simulated = canvas.create_oval(400, 400, 405, 405, fill='blue')
root.update()

def find_acceleration(x1,my_xs,q1,my_qs,real_distance):
    global ke
    global m
    acceleration = 0
    direction = 1
    for i in range (len(my_xs)):
        try:
            distance = x1 - my_xs[i] 
            print(distance)
            print("Is the distance \n")
            if (distance < 0):
                direction = -1
            acceleration += (distance*ke*q1*my_qs[i])/((real_distance[i]**3)*m)
        except ZeroDivisionError:
            acceleration += 0
    print("Calculating acceleration " + str(acceleration))
    #print(ke,x1,q1,my_xs,my_qs,m)
    return acceleration

def find_velocity (vi,a):
    vf = vi + a*dt
    print("Calculating velocity " + str(vf))
    return vf
def find_position(xi, vi):
    xf = xi + vi*dt
    print("Calculating position " + str(xf))
    return xf



random.seed()

    
x = 500
y = 500
q = 10
vx = random.randint(-50,50)
vy = random.randint(-50,50)
dt = 0.01
energy_loss_x = 0.99
energy_loss_y = 1.01

charges_value = [10,-5, -10, random.randint(-20,-5),0,0,0]
charges_x = [600,500,200, random.randint(100,1000),0,0,0]
charges_y = [500,400,400,random.randint(100,700),0,0,0]
true_distances = [0,0,0,0,0,0,0]

def spawn_charges():
    j = random.randint(2,7)
    for i in range(j):
        my_choice = [random.randint(-20,-5),random.randint(-20,-5),random.randint(5,20)]
        charges_value[i] = random.choice(my_choice)
        charges_x[i] = random.randint(100,1200)
        charges_y[i] = random.randint(100,700)
    if ((len(charges_x) - j - 1) > 0):
        for i in range(j, len(charges_x)-1):
            charges_value[i] = 0
            charges_x[i] = -200
            charges_y[i] = -200
    for i in range(len(charges_x)):
        if (charges_value[i] < 0):
            s = canvas.create_oval(charges_x[i] - 5, charges_y[i] - 5, charges_x[i] + 5, charges_y[i] + 5, fill='red')
            charges_simulated.append(s)
        else:
            s = canvas.create_oval(charges_x[i] - 5, charges_y[i] - 5, charges_x[i] + 5, charges_y[i] + 5, fill='green')
            charges_simulated.append(s)
    print(str(charges_x[i])+str(charges_y[i]) + "those are the coordinates" )
    root.update()
    return


charges_simulated = []

spawn_charges()
for i in range(len(charges_x)):
    if (charges_value[i] < 0):
        s = canvas.create_oval(charges_x[i] - charges_value[i]/2, charges_y[i] - charges_value[i]/2, charges_x[i] + charges_value[i]/2, charges_y[i] + charges_value[i]/2, fill='red')
        charges_simulated.append(s)
    else:
        s = canvas.create_oval(charges_x[i] - charges_value[i]/2, charges_y[i] - charges_value[i]/2, charges_x[i] + charges_value[i]/2, charges_y[i] + charges_value[i]/2, fill='green')
        charges_simulated.append(s)
    print(str(charges_x[i])+str(charges_y[i]) + "those are the coordinates" )
root.update()

skip = 0
for i in range (0,200000):
    move_to(x,y)
    print("this is x \n")

    for i in range (len(charges_x)):
        true_distances[i] = math.sqrt((charges_x[i]-x)**2 + (charges_y[i]-y)**2)
        print("Distancezzz")
        print(true_distances[i],i)
        if (true_distances[i] <= 15):
            skip = 1
    if (skip ==1):
        vx = -vx*energy_loss_x
        vy = -vy*energy_loss_y
        x = find_position(x,vx)
        y = find_position(y,vy)
        print("Reversing position")
        time.sleep(0.1)
        skip = 0
        continue
    ax = find_acceleration(x,charges_x,q,charges_value,true_distances)
    if (ax > 10000):
        ax = 1000
        print("acceleration was way too big ! \n")
        time.sleep(1)
    elif ( ax < - 10000):
        ax = 1000
        print("acceleration was way too big ! \n")
        time.sleep(0.1)
    vx = find_velocity(vx,ax)
    x = find_position(x,vx)
    print("this is y \n")

    ay = find_acceleration(y,charges_y,q,charges_value,true_distances)
    print("The acceleration is" + str(ay))
    vy = find_velocity(vy,ay)
    y = find_position(y,vy)
    time.sleep(0.005)

