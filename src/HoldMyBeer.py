import keyboard
import mss
import os
import pystray
import threading
import tkinter as tk

from PIL import Image, ImageDraw, ImageTk, ImageEnhance
from region_selector import RegionSelector

def capture_region():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            shot = sct.grab(monitor)
            original_frozen_image = Image.frombytes("RGB", shot.size, shot.rgb)
            frozen_image = ImageEnhance.Brightness(
                original_frozen_image
            ).enhance(0.75)
        
        root.after(
            0,
            lambda: RegionSelector(
                tk.Toplevel(root),
                original_frozen_image,
                frozen_image,
                monitor
            )
        )
    except Exception as e:
        print(e)

def create_tray_icon():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), outline="red", width=4)

    menu = pystray.Menu(
        pystray.MenuItem("Capture Region", lambda _: capture_region()),
        pystray.MenuItem("Exit", lambda _: exit_app())
    )

    icon = pystray.Icon("screenshot", image, "Hold My Beer (Screenshot tool) by @youugotssponged", menu)
    global tray_icon
    tray_icon = icon
    icon.run()

def exit_app():
    keyboard.unhook_all()
    tray_icon.stop()
    root.destroy()
    os._exit(0)

def setup_hotkey():
    keyboard.add_hotkey("alt+print_screen", capture_region)

##################################################################################################################################

tray_icon = None
root = None # will act as the 'drawable overlay surface', hidden but allowing tk to spawn child windows for image preview

def main():
    global root
    root = tk.Tk()
    root.withdraw()

    setup_hotkey()
    threading.Thread(target=create_tray_icon, daemon=True).start() # to stop pystray Icon method call from blocking the main thread when creating the tray icon on windows
    
    root.mainloop()

if __name__ == "__main__":
    main()