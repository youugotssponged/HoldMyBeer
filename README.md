# Hold My Beer
## Super lightweight simple screenshot utility 
### Made for Windows & for a friend who wanted something slightly different than other screenshot tools

## To use
- Double click HoldMyBeerScreenshot.exe, notice that it has now started silently and populated in your icon tray on your windows taskbar on the bottom right.

- ALT + PRINTSCREEN to activate the screenshot overlay
    - Click and drag to take a screenshot
    - ESC or Right Click to cancel

OR ALTERNATIVELY

- Right click the Hold my beer icon in your system tray and choose 'Capture region'


THATS ALL THERE IS!!!

Well, you can also copy the screenshot to your clipboard or save it to your desktop with the copy and save options found at the top of the screenshot window.


Have fun!


# Development notes

Built with Pyinstaller, please refer to ```./HoldMyBeer.spec```
Deps: tkinter, pystray, mss, keyboard, pyperclipimg, pillow

- TODO: Cleanup/Refactor HoldMyBeer.py as this was done in one night up til 4am based