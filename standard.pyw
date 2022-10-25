dir = "F:\Downloads\Live-Wallpaper-main\Live-Wallpaper-main" + "\\"

import ctypes, datetime, sched, time, math, json
import os
import pathlib

def config():
    load = open(dir + 'config.json')
    configData = json.load(load)
    directory = dir + configData['imagesPath']
    print(directory)
    if (dir == ""):
        directory = f'{pathlib.Path().resolve()}\{directory}'
    timeslist = dir + configData['timesList']
    timeslist = open(timeslist)
    timeslist = json.load(timeslist)

    sunRise_Start = timeslist['sunRise_Start']
    day_Start = timeslist['day_Start']
    sunSet_Start = timeslist['sunSet_Start']
    night_Start = timeslist['night_Start']
    framesForTime = timeslist['framesForTime']
    backgroundUpdateTimer = sched.scheduler(time.time, time.sleep)
    
    now = datetime.datetime.now()
    month = math.ceil((int(now.strftime("%m")) - 1))
    currentSec = 0
    waitForNextFrame = 0
    timeSinceSync = 0
    currentFrame = 0

    return directory, timeslist, sunRise_Start, day_Start, sunSet_Start, night_Start, framesForTime, backgroundUpdateTimer, now, month, currentSec, waitForNextFrame, timeSinceSync, currentFrame

directory, timeslist, sunRise_Start, day_Start, sunSet_Start, night_Start, framesForTime, backgroundUpdateTimer, now, month, currentSec, waitForNextFrame, timeSinceSync, currentFrame = config()


def waitTime():
    global waitForNextFrame, timeArea, currentSec
    now = datetime.datetime.now()
    currentSec = int(now.strftime("%H")) * 3600 + int(now.strftime("%M")) * 60 + int(now.strftime("%S"))

    if currentSec >= night_Start[month]: #night before 00:00
        waitForNextFrame = (86400 - night_Start[month])
        timeArea = 3
    elif currentSec < sunRise_Start[month]: #night after 00:00
        waitForNextFrame = (sunRise_Start[month])
        timeArea = 4
    elif currentSec < day_Start[month]: #sunrise
        waitForNextFrame = (day_Start[month] - sunRise_Start[month])
        timeArea = 0
    elif currentSec < sunSet_Start[month]: #day
        waitForNextFrame = (sunSet_Start[month] - day_Start[month])
        timeArea = 1
    elif currentSec < night_Start[month]: #sunset
        waitForNextFrame = (night_Start[month] - sunSet_Start[month])
        timeArea = 2
    waitForNextFrame = waitForNextFrame / 3600 / framesForTime[timeArea] * 3600


def startFrame():
    global currentFrame, month

    now = datetime.datetime.now()
    currentSec = int(now.strftime("%H")) * 3600 + int(now.strftime("%M")) * 60 + int(now.strftime("%S"))
    
    if timeArea == 0:
        currentFrame = int(math.ceil((currentSec - sunRise_Start[month]) / waitForNextFrame)) -30
    elif timeArea == 1:
        currentFrame = int(math.ceil((currentSec - day_Start[month]) / waitForNextFrame)) + 40
    elif timeArea == 2:
        currentFrame = int(math.ceil((currentSec - sunSet_Start[month]) / waitForNextFrame)) + 680
    elif timeArea == 3:
        currentFrame = int(math.ceil((currentSec - night_Start[month]) / waitForNextFrame)) + 760
    elif timeArea == 4:
        currentFrame = int(math.ceil((currentSec / waitForNextFrame))) + 760
    
    currentFrame -= 1
    updateBG()


def updateBG():
    global currentFrame, timeSinceSync

    currentFrame += 1
    imageName = str(currentFrame)
    while len(imageName) < 5:
        imageName = "0" + imageName
    imageDirectory = directory + "/" + imageName + ".png"

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imageDirectory)

    timeSinceSync += waitForNextFrame
    print(waitForNextFrame, " | ",  imageDirectory, " | ", timeArea)
    if (timeSinceSync >= 3600):
        timeSinceSync = 0
        print("Syncing")
        startFrame()
    else:
        backgroundUpdateTimer.enter(waitForNextFrame, 1, updateBG) #waitForNextFrame
        backgroundUpdateTimer.run()


waitTime()
startFrame()