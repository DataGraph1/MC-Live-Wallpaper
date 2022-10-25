import ctypes, requests, datetime, sched, time, math, json

f = open("Directories.txt", "r")
directory = f.readline()
timelist = f.readlines()
timelist = timelist[0]
f.close()
print("Times", timelist)
f = open(timelist)
data = json.load(f)
sunRise_Start = []
for i in data["sunRise_Start"]:
    sunRise_Start += i
print(sunRise_Start)


#with open(timelist, "r") as f:
sunRise_Start = json.load(f)
day_Start = [28800,27900,24300,24300,20700,17100,17100,19800,22500,25200,25200,27900]
sunSet_Start = [57600,61200,64800,70200,73800,75600,76500,75600,72000,67500,60300,57600]
night_Start = [60300,63000,66600,72000,75600,79200,80100,77400,73200,69300,61200,60300]
framesForTime = [80, 640, 80, 660, 660] #sunRise frames, sun frames, sunSet frames, night frames

backgroundUpdateTimer = sched.scheduler(time.time, time.sleep)

now = datetime.datetime.now()
month = math.ceil((int(now.strftime("%m")) - 1))
currentSec = 0
waitForNextFrame = 0
timeSinceSync = 0
currentFrame = 0
weather = "Sunny"


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


def weathTest():
    global weather
    CITY = "" #CITY
    API_KEY = "" #API_KEY
    URL = "https://api.openweathermap.org/data/2.5/weather?q=" + CITY + "&appid=" + API_KEY

    response = requests.get(URL)
    data = response.json()
    main = data['main']
    report = data['weather']

    if f"{report[0]['description']}" == "clear sky" or f"{report[0]['description']}" == "few clouds":
        weather == "Sunny"
    elif f"{report[0]['description']}" == "scattered clouds" or f"{report[0]['description']}" == "broken clouds" or f"{report[0]['description']}" == "overcast clouds" or f"{report[0]['description']}" == "mist":
        weather = "Cloudy"
    elif f"{report[0]['description']}" == "shower rain" or f"{report[0]['description']}" == "rain" or f"{report[0]['description']}" == "thunderstorm" or f"{report[0]['description']}" == "shower rain":
        weather = "Rainy"
    elif f"{report[0]['description']}" == "snow":
        weather = "Snowy"
    print(f"{report[0]['description']}")

        
def updateBG():
    #weathTest()
    global currentFrame, timeSinceSync

    currentFrame += 1
    imageName = str(currentFrame)
    while len(imageName) < 5:
        imageName = "0" + imageName
    imageDirectory = directory + "/" + weather + "/" + imageName + ".png"

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