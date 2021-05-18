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
            x = (y / math.tan(math.radians(-2.6))) / 6076.12
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
    calcButtonDeg = tk.Button(todWindow, text="-2.6 degree FPA", command=calcTodDegrees)
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
    def pickAirport(minTime,maxTime,lat,lon):
        airportsListJson = open("airports.json", encoding='cp850')
        airportsList = json.load(airportsListJson)
        icaos = open("icaos.txt", "r").read()
        icaoList = icaos.split(",")
        if minTime:
            minDist = (minTime*500)-200
            maxDist = (maxTime*500)+200
            airportCords1 = (lat,lon)
            foundAirports = []
            for i in icaoList:
                airport = airportsList[i]
                if airport["lat"] and airport["lon"]:
                    airportCords2 = (airport["lat"], airport["lon"])
                    actDist = haversine(airportCords1,airportCords2,unit="mi")
                    if minDist < actDist < maxDist:
                        foundAirports.append(airport)
            if len(foundAirports) != 0:
                airP = foundAirports[numpy.random.randint(0,len(foundAirports))]
                return airP
            else: return None
        else:
            randomNum = numpy.random.randint(0, len(icaoList))
            airport = airportsList[icaoList[randomNum]]
            print(icaoList[randomNum])
            return airport
    def genRoute():
        airportsListJson = open("airports.json", encoding='cp850')
        airportsList = json.load(airportsListJson)
        airportS = airportEntry.get()
        outputLabel.config(text="No Valid Routes Exist")
        if airportS == "":
            timeEntered = timeEntry.get()
            minTime = None
            maxTime = None
            if len(timeEntered.split("-"))==2:
                minTime = float(timeEntered.split("-")[0])
                maxTime = float(timeEntered.split("-")[1])
            else:
                minTime = float(timeEntered)
                maxTime = float(timeEntered)
            airport = None
            secondAirport=None
            y=0
            while secondAirport is None and y<50:
                airport = pickAirport(None,None,None,None)
                secondAirport=pickAirport(minTime,maxTime,float(airport["lat"]),float(airport["lon"]))
                y+=1
            outputLabel.config(text=airport["icao"] + " -> " + secondAirport["icao"])
        else:
            time = float(timeEntry.get())
            distance = time * 500
            airport = airportsList[airportS]
            secondAirport = None
            if airport:
                secondAirport = pickAirport(distance, float(airport["lat"]), float(airport["lon"]))
            outputLabel.config(text=airport["icao"] + " <-> " + secondAirport["icao"])
    routeWindow = tk.Tk()
    routeWindow.title("Flight Generator")
    thisTitleLabel = tk.Label(routeWindow,text="Flight Generator")
    thisTitleLabel.grid(row=0,column=1)
    timeLabel = tk.Button(routeWindow,text="Time (Hours)",command=genRoute)
    timeLabel.grid(row=1,column=0)
    timeEntry = tk.Entry(routeWindow)
    timeEntry.grid(row=1,column=2)
    airportEntry = tk.Entry(routeWindow)
    airportEntry.grid(row=2,column=2)
    aiportLabel = tk.Label(routeWindow,text="Airport (Optional)")
    aiportLabel.grid(row=2,column=0)
    outputLabel = tk.Label(routeWindow,text="Enter a Time and press the button")
    outputLabel.grid(row=3,column=1)
    routeWindow.mainloop()
def settings():
    def addAirport():
        airportsListJson = open("airports.json", encoding='cp850')
        airportsList1 = json.load(airportsListJson)
        icaos = open("icaos.txt","a")
        icaos2 = open("icaos.txt","r")
        icaosList = icaos2.read().split(",")
        enty = airportEntry.get()
        ableToAdd = True
        for i in icaosList:
            if i == enty:
                ableToAdd = False
                break
        found = False
        if ableToAdd is True:
            for i in airportsList1:
                if i == enty:
                    found = True
                    break
        if ableToAdd is True and found is True:
            icaos.write(","+enty)
            infoLabel.config(text=enty+" has been successfully added")
        else:
            infoLabel.config(text="Something when wrong, make sure you entered a valid icao")
        airportEntry.delete(0,'end')
        icaos.close()
        icaos2.close()
    settingsWindow = tk.Tk()
    settingsWindow.title("Settings")
    addAirportButton = tk.Button(settingsWindow,text="Add Airport",command=addAirport)
    addAirportButton.grid(row=0,column=0)
    airportEntry = tk.Entry(settingsWindow)
    airportEntry.grid(row=0,column=1)
    infoLabel = tk.Label(settingsWindow,text="Enter an Icao")
    infoLabel.grid(row=1,column=0)
    settingsWindow.mainloop()
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
settingsButton = tk.Button(masterWindow,text="Settings",font=("Arial",20),command=settings)
settingsButton.grid(row=4,column=0)
masterWindow.mainloop()
