# Hold My Beer

A lightweight, no-fuss screenshot utility for Windows that lives in your system tray. Press **Alt + Print Screen**, drag to select, and you're done — no splash screens, no config dialogs, no bloat.

## Features

- **Instant region capture** — `Alt + Print Screen` triggers a full-screen dimmed overlay; click and drag to select any area
- **Live preview** — selected region is brightened in real time against the dimmed background
- **Cancel anytime** — press `Esc` or right-click to dismiss
- **System tray daemon** — starts silently, runs in the background, accessible from the notification area
- **Clipboard or file** — captured regions can be copied directly to clipboard (`pyperclipimg`) or saved to disk as PNG/JPEG
- **Multi-monitor aware** — overlay spans all monitors using a virtual screen coordinate space

## Usage

1. Launch `HoldMyBeerScreenshot.exe` — it minimises to the system tray.
2. Press **Alt + Print Screen** (or right-click the tray icon → *Capture Region*).
3. Click and drag to select a region; release to capture.
4. In the preview window, use **File → Copy to clipboard** or **File → Save As**.

## Development

Built with Python and packaged via PyInstaller. See `HoldMyBeer.spec` for build configuration.

**Dependencies:** `tkinter`, `pystray`, `mss`, `keyboard`, `pyperclipimg`, `pillow`

```bash
pip install pystray mss keyboard pyperclipimg pillow
```