import threading
import tkinter as tk
import pystray
import mss
import keyboard
import os
import pyperclipimg as pci

from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk, ImageEnhance

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

class RegionSelector:
    def __init__(self, overlay, screenshot, screenshot_dimmed, monitor):
        self.root = overlay
        self.screenshot = screenshot
        self.screenshot_dimmed = screenshot_dimmed
        self.highlight_image_id = None
        self.highlight_tk_img = None

        self.virtual_monitor = monitor
        self.start_x = self.start_y = 0
        self.rect = None

        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<ButtonPress-3>", lambda e: self.root.destroy())

        # Get virtual monitor covering all screens
        # Make overlay cover all monitors
        self.root.geometry(
            f"{self.virtual_monitor['width']}x{self.virtual_monitor['height']}+{self.virtual_monitor['left']}+{self.virtual_monitor['top']}"
        )

        self.tk_bg = ImageTk.PhotoImage(self.screenshot_dimmed)
        
        self.canvas = tk.Canvas (
            self.root, 
            cursor="cross", 
            highlightthickness=0
        )

        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_image (
            0, 
            0, 
            image=self.tk_bg,
            anchor="nw"
        )

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Escape>", lambda e: self.root.destroy())
        self.root.focus_force()

    def remove_stale_highlight(self):
        if self.highlight_image_id is not None:
            self.canvas.delete(self.highlight_image_id)
            self.highlight_tk_img = None

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline="red", width=2
        )
        self.remove_stale_highlight()

    def on_drag(self, event):
        self.canvas.coords(
            self.rect,
            self.start_x, self.start_y,
            event.x, event.y
        )
        self.remove_stale_highlight()

        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        w, h = int(x2 - x1), int(y2 - y1)

        if w > 0 and h > 0:
            bright_region = self.screenshot.crop((int(x1), int(y1), int(x2), int(y2)))
            self.highlight_tk_img = ImageTk.PhotoImage(bright_region)
            self.highlight_image_id = self.canvas.create_image(
                int(x1), 
                int(y1),
                image=self.highlight_tk_img,
                anchor="nw"
            )
            # force red outline visibility on top
            self.canvas.tag_lower(self.highlight_image_id, self.rect)

    def on_release(self, event):
        self.remove_stale_highlight()
        
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Convert coordinates
        left = int(min(x1, x2))
        top = int(min(y1, y2))
        right = int(max(x1, x2))
        bottom = int(max(y1, y2))

        cropped = self.screenshot.crop (
            (left, top, right, bottom)
        )

        self.root.destroy()
        show_image(cropped)
        

def show_image(img):
    window = tk.Toplevel(root)

    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=False)

    menu_bar.add_cascade(label="File", menu = file_menu)
    file_menu.add_command(label="Copy to clipboard", command = lambda: pci.copy(img))
    file_menu.add_command(label='Save As', command = lambda: saveImage(image=img))
    file_menu.add_command(label='Exit', command = window.destroy)
    
    tk_img = ImageTk.PhotoImage(img)    
    label = tk.Label(window, image=tk_img)
    label.image = tk_img
    label.pack()

    window.title("Hold My Beer - Captured Region")
    window.config(menu=menu_bar)    
    window.resizable(False, False)  # Disable window resizing

def saveImage(image):
    filename = filedialog.asksaveasfilename (
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )

    if filename:
        image.save(filename)

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