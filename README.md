# Live-Wallpaper

Installation

Initional setup
1. Go to python.org/downloads and click "Download Python"
2. Run the the downloaded program
3. Click "Install Now"
4. Click "Yes" on the pop-up
5. Download "TimeList.json", "WallPaperChanger.pyw" & "Compressed Images" from the GitHub repository at github.com/DataGraph1/Live-Wallpaper
6. Run "WallPaperChanger.pyw"

Run on PC start up
1. Press "Windows" and "R" and type "%AppData%"
2. Go to Microsoft > Windows > Start Menu > Programs > Startup
3. Move "WallPaperChanger.pyw" into the folder
4. Right-Click "WallPaperChanger.pyw" and click Open With > Notepad
5. Change line 1 to dir = "[the directory to you other files]"

Making your own wallpapers
1. Download a macro creator and make a macro to press F2 every minute
2. Go somewhere in Minecraft, press F1 and F11 (to full screen)
3. Run macro for 20 minutes (full day and night in MC)
4. Replace the photos in the "Compressed Images" folder with your screenshots (there should be 1440)

Turning on weather (more technical)
1. Install the requests package (pip install requests)
2. Go to openweathermap.org, create an account and get your API token
3. Input your token into "API_KEY" on line 82
4. Input your city into "CITY" on line 81
5. Remove "#" from "#weather()" on line 102
