import tkinter as tk
from SimConnect import *
import math
import json as json
import numpy
from functools import cache
from haversine import haversine, Unit
def openTod():
    def calcTodDegrees():
        try:
            sm = SimConnect()
            aq = AircraftRequests(sm)
            finalAlt = float(finalAltEntry.get())
            alt = aq.get("PLANE_ALTITUDE")
            y = finalAlt - alt
            x = (y / math.tan(math.radians(-3))) / 6076.12
            sm.exit()
            todLabel.config(text="Descent Distance " + str(math.floor(x)))
        except Exception:
            todLabel.config(text="Could not connect to simulator!")

    def calcTodVert():
        try:
            sm = SimConnect()
            aq = AircraftRequests(sm)
            vertSpeed = float(vertSpeedEntry.get())
            groundSpeed = aq.get("GROUND_VELOCITY")
            alt = aq.get("PLANE_ALTITUDE")
            finalAlt = float(finalAltEntry.get())
            y = alt - finalAlt
            distance = ((y / vertSpeed) / 60) * groundSpeed
            todLabel.config(text="Descent Distance: " + str(math.floor(distance)))
            sm.exit()
        except Exception:
            todLabel.config(text="Could not connect to simulator!")

    def calcTodDist():
        try:
            sm = SimConnect()
            aq = AircraftRequests(sm)
            alt = aq.get("PLANE_ALTITUDE")
            groundSpeed = aq.get("GROUND_VELOCITY")
            finalAlt = float(finalAltEntry.get())
            dist = float(distanceEntry.get())
            y = alt - finalAlt
            vertSpeed = (y * groundSpeed) / (dist * 60)
            todLabel.config(text="Vertical Speed: " + str(math.floor(vertSpeed)))
        except Exception:
            todLabel.config(text="Could not connect to simulator!")


    todWindow = tk.Tk()
    todWindow.title("Descent Calculator")
    enterFinalAlt = tk.Label(todWindow, text="Enter Final Alt")
    enterFinalAlt.grid(row=0, column=0)
    finalAltEntry = tk.Entry(todWindow)
    finalAltEntry.grid(row=0, column=2)
    desiredVertSpeed = tk.Label(todWindow, text="Enter Vertical Speed")
    desiredVertSpeed.grid(row=1, column=0)
    vertSpeedEntry = tk.Entry(todWindow)
    vertSpeedEntry.grid(row=1, column=2)
    desiredDistance = tk.Label(todWindow, text="Enter Desired Distance")
    desiredDistance.grid(row=2, column=0)
    distanceEntry = tk.Entry(todWindow)
    distanceEntry.grid(row=2, column=2)
    calcButtonDeg = tk.Button(todWindow, text="-3 degree FPA", command=calcTodDegrees)
    calcButtonDeg.grid(row=3, column=0)
    calcButtonVert = tk.Button(todWindow, text="Vertical Speed", command=calcTodVert)
    calcButtonVert.grid(row=3, column=1)
    calcButtonDist = tk.Button(todWindow, text="Distance", command=calcTodDist)
    calcButtonDist.grid(row=3, column=2)
    todLabel = tk.Label(todWindow, text=".      Enter Information      .")
    todLabel.grid(row=4, column=1)
    todWindow.mainloop()

def openLoader():
    def kgToPounds(kgs):
        lbs = kgs * 2.205
        return lbs

    def poundsToKgs(lbs):
        kgs = lbs / 2.205
        return kgs

    def kgClick():
        try:
            kgs = float(kgEntry.get())
            sm = SimConnect()
            ae = AircraftEvents(sm)
            ar = AircraftRequests(sm)
            setFuel = ae.find("ADD_FUEL_QUANTITY")
            totalQuantity = ar.get("FUEL_TOTAL_QUANTITY")
            totalCapacitygal = ar.get("FUEL_TOTAL_CAPACITY")
            weightPerGallon = ar.get("FUEL_WEIGHT_PER_GALLON")
            totalCapacity = totalCapacitygal * weightPerGallon
            lbs = kgToPounds(kgs)
            fuelToAdd = (lbs / totalCapacity) * 65535
            print(lbs)
            print(totalCapacity)
            print(totalQuantity)
            print(fuelToAdd)
            setFuel(int(fuelToAdd))
            sm.exit()
            fuelLabel.config(text="Fuel Loaded!")
        except Exception:
            fuelLabel.config(text="Could not connect to sim!")

    def lbsClick():
        try:
            lbs = float(lbsEntry.get())
            sm = SimConnect()
            ae = AircraftEvents(sm)
            ar = AircraftRequests(sm)
            setFuel = ae.find("ADD_FUEL_QUANTITY")
            totalQuantity = ar.get("FUEL_TOTAL_QUANTITY")
            totalCapacitygal = ar.get("FUEL_TOTAL_CAPACITY")
            weightPerGallon = ar.get("FUEL_WEIGHT_PER_GALLON")
            totalCapacity = totalCapacitygal * weightPerGallon
            fuelToAdd = (lbs / totalCapacity) * 65535
            print(totalCapacity)
            print(totalQuantity)
            print(fuelToAdd)
            setFuel(int(fuelToAdd))
            sm.exit()
            fuelLabel.config(text="Fuel Loaded!")
        except Exception:
            fuelLabel.config(text="Could not connect to sim!")
    mainWindow = tk.Tk()
    mainWindow.title("Fuel Loader")
    fuelLabel = tk.Label(mainWindow,text="Fuel",font=("Arial",20))
    fuelLabel.grid(row=0,column=1)
    kgButton = tk.Button(mainWindow, text="Kg", font=("Arial", 20), command=kgClick)
    kgButton.grid(row=1, column=0)
    kgEntry = tk.Entry(mainWindow, font=("Arial", 20))
    kgEntry.grid(row=1, column=1)
    lbsButton = tk.Button(mainWindow, text="lbs", font=("Arial", 20), command=lbsClick)
    lbsButton.grid(row=2, column=0)
    lbsEntry = tk.Entry(mainWindow, font=("Arial", 20))
    lbsEntry.grid(row=2, column=1)
    mainWindow.mainloop()

def routeDecider():
    def calcDist(lat1,lon1,lat2,lon2):
        R = 3440.1
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    @cache
    def pickAirport(dist,lat,lon):
        if dist:
            airP = None
            airportCords1 = (lat,lon)
            x=0
            while airP is None and x<300:
                x+=1
                randomNum = numpy.random.randint(0, len(icaoList))
                airport = airportsList[icaoList[randomNum]]
                if airport["lat"] and airport["lon"]:
                    airportCords2 = (airport["lat"], airport["lon"])
                    actDist = haversine(airportCords1,airportCords2,unit="mi")
                    print(airport["icao"],actDist)
                    if dist-100 < actDist < dist+100:
                        print("OWWHHHH GAWWD")
                        airP = airport
            return airP
        else:
            randomNum = numpy.random.randint(0, len(icaoList))
            airport = airportsList[icaoList[randomNum]]
            print(icaoList[randomNum])
            return airport


    def genRoute():
        outputLabel.config(text="Error! Please reload the Flight Generator Window!")
        global airportsList
        time = float(timeEntry.get())
        distance = time*500
        airport = pickAirport(None,None,None)
        secondAirport=pickAirport(distance,float(airport["lat"]),float(airport["lon"]))
        outputLabel.config(text=airport["icao"] + " -> " + secondAirport["icao"])

    routeWindow = tk.Tk()
    routeWindow.title("Flight Generator")
    thisTitleLabel = tk.Label(routeWindow,text="Flight Generator")
    thisTitleLabel.grid(row=0,column=1)
    timeLabel = tk.Button(routeWindow,text="Time (Hours)",command=genRoute)
    timeLabel.grid(row=1,column=0)
    timeEntry = tk.Entry(routeWindow)
    timeEntry.grid(row=1,column=2)
    outputLabel = tk.Label(routeWindow,text="Enter a Time and press the button")
    outputLabel.grid(row=2,column=1)
    routeWindow.mainloop()
airportsListJson = open("airports.json",encoding='cp850')
airportsList = json.load(airportsListJson)
icaos = open("icaos.txt","r").read()
icaoList = icaos.split(",")
masterWindow = tk.Tk()
masterWindow.title("Zakiack's MSFS EFB")
titleLabel = tk.Label(masterWindow,text="MSFS EFB",font=("Arial",20))
titleLabel.grid(row=0,column=0)
todCalcButton = tk.Button(masterWindow,text="Descent Calculator",font=("Arial",20),command=openTod)
todCalcButton.grid(row=1,column=0)
loaderButton = tk.Button(masterWindow,text="Weight and Balance",font=("Arial",20),command=openLoader)
loaderButton.grid(row=2,column=0)
routeDecButton = tk.Button(masterWindow,text="Flight Generator",font=("Arial",20),command=routeDecider)
routeDecButton.grid(row=3,column=0)
masterWindow.mainloop()
