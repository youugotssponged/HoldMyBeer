import threading
import tkinter as tk
import pystray
import mss
import keyboard
import os
import pyperclipimg as pci

from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk


# ---------- Screenshot logic ----------
def capture_region():
    # Schedule overlay creation on the main Tkinter thread
    if root:
        root.after(0, lambda: RegionSelector(tk.Toplevel(root)))


    #### Spongy note to self: tkinter isn't thread safe and this is just unneccessary! ####
    # def run():
    #    overlay = tk.Toplevel(root) 
    #    RegionSelector(overlay)
    # 
    # threading.Thread(target=run, daemon=True).start() 
    #######################################################################################

class RegionSelector:
    def __init__(self, overlay):
        self.root = overlay
        self.start_x = self.start_y = 0
        self.rect = None

        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<ButtonPress-3>", lambda e: self.root.destroy())

        # Get virtual monitor covering all screens
        with mss.mss() as sct:
            self.virtual_monitor = sct.monitors[0]

        # Make overlay cover all monitors
        self.root.geometry(
            f"{self.virtual_monitor['width']}x{self.virtual_monitor['height']}+{self.virtual_monitor['left']}+{self.virtual_monitor['top']}"
        )

        self.canvas = tk.Canvas(self.root, bg="black", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline="red", width=2
        )

    def on_drag(self, event):
        self.canvas.coords(
            self.rect,
            self.start_x, self.start_y,
            event.x, event.y
        )

    def on_release(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Convert coordinates relative to virtual monitor
        left = int(min(x1, x2) + self.virtual_monitor['left'])
        top = int(min(y1, y2) + self.virtual_monitor['top'])
        width = int(abs(x2 - x1))
        height = int(abs(y2 - y1))

        self.root.destroy()
        grab_and_show(left, top, width, height)

def grab_and_show(left, top, width, height):
    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }

        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        show_image(img)

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
    window.bind("<Escape>", lambda e: window.destroy())
    window.resizable(False, False)  # Disable window resizing

def saveImage(image):
    filename = filedialog.asksaveasfilename (
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )

    if filename:
        image.save(filename)

# ---------- Tray icon ----------

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

# ---------- Global hotkey ----------

def setup_hotkey():
    keyboard.add_hotkey("alt+print_screen", capture_region)

# ---------- Main ----------

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