import os
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw, ImageFont
from tkinter import simpledialog, messagebox
from screenshot_button.screenshot_button import ScreenshotButton


if __name__ == "__main__":
    # Create an instance of the ScreenshotButton class
    screenshot_button = ScreenshotButton()

    # Set up the main window
    screenshot_button.master.title("Screenshot Button")

    # Create the Quit button
    quit_button = tk.Button(screenshot_button.master, text="Quit", command=screenshot_button.quit_application)
    quit_button.pack()

    # Pack the ScreenshotButton
    screenshot_button.pack()

    # Run the Tkinter main loop
    screenshot_button.master.mainloop()
