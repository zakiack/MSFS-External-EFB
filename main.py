from SimConnect import *
import tkinter as tk
import math
def calcTodDegrees():
    sm = SimConnect()
    aq = AircraftRequests(sm)
    finalAlt = float(finalAltEntry.get())
    alt = aq.get("PLANE_ALTITUDE")
    y = finalAlt-alt
    x = (y/math.tan(math.radians(-3)))/6076.12
    sm.exit()
    todLabel.config(text="Descent Distance "+str(math.floor(x)))
def calcTodVert():
    sm = SimConnect()
    aq = AircraftRequests(sm)
    vertSpeed = float(vertSpeedEntry.get())
    groundSpeed = aq.get("GROUND_VELOCITY")
    alt = aq.get("PLANE_ALTITUDE")
    finalAlt = float(finalAltEntry.get())
    y = alt-finalAlt
    distance = ((y/vertSpeed)/60)*groundSpeed
    todLabel.config(text="Descent Distance: "+str(math.floor(distance)))
    sm.exit()
def calcTodDist():
    sm = SimConnect()
    aq = AircraftRequests(sm)
    alt=aq.get("PLANE_ALTITUDE")
    groundSpeed = aq.get("GROUND_VELOCITY")
    finalAlt = float(finalAltEntry.get())
    dist = float(distanceEntry.get())
    y=alt-finalAlt
    vertSpeed = (y*groundSpeed)/(dist*60)
    todLabel.config(text="Vertical Speed: "+str(math.floor(vertSpeed)))
masterWindow = tk.Tk()
masterWindow.title("Descent Calculator")
enterFinalAlt = tk.Label(masterWindow,text="Enter Final Alt")
enterFinalAlt.grid(row=0,column=0)
finalAltEntry = tk.Entry(masterWindow)
finalAltEntry.grid(row=0,column=2)
desiredVertSpeed = tk.Label(masterWindow,text="Enter Vertical Speed")
desiredVertSpeed.grid(row=1,column=0)
vertSpeedEntry = tk.Entry(masterWindow)
vertSpeedEntry.grid(row=1,column=2)
desiredDistance = tk.Label(masterWindow,text="Enter Desired Distance")
desiredDistance.grid(row=2,column=0)
distanceEntry = tk.Entry(masterWindow)
distanceEntry.grid(row=2,column=2)
calcButtonDeg = tk.Button(masterWindow,text="-3 degree FPA",command=calcTodDegrees)
calcButtonDeg.grid(row=3,column=0)
calcButtonVert = tk.Button(masterWindow,text="Vertical Speed",command=calcTodVert)
calcButtonVert.grid(row=3,column=1)
calcButtonDist = tk.Button(masterWindow,text="Distance",command=calcTodDist)
calcButtonDist.grid(row=3,column=2)
todLabel = tk.Label(masterWindow,text="Enter Information")
todLabel.grid(row=4,column=1)
masterWindow.mainloop()