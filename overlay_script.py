# overlay_script.py

import os
import tkinter as tk
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import pyautogui
from tkinter import simpledialog  # Import simpledialog directly

from image_processing.image_processing import create_step

class ScreenshotButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, text="Capture Screenshot", command=self.capture_screenshot, **kwargs)

    def capture_screenshot(self):
        # Hide the button temporarily
        self.pack_forget()

        # Capture the entire screen
        screenshot = ImageGrab.grab()

        # Show the button again
        self.pack()

        # Ask the user for a caption using simpledialog
        caption = simpledialog.askstring("Caption", "Enter a caption for this step:")

        # Save the screenshot to the output folder
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        filename = os.path.join(output_folder, f"step_{self.step_counter}.png")
        screenshot.save(filename)

        # Create step with caption
        image = Image.open(filename)
        image_with_caption = create_step(image, caption)
        image_with_caption.save(filename)

        print(f"Step {self.step_counter} captured and saved as {filename}")

        # Increment the step counter
        self.step_counter += 1

    def run(self):
        self.step_counter = 1

        # Set up the main window
        self.master.title("Screenshot Button")
        self.pack()

        # Run the Tkinter main loop
        self.master.mainloop()

if __name__ == "__main__":
    # Create an instance of the ScreenshotButton class
    screenshot_button = ScreenshotButton()

    # Run the application
    screenshot_button.run()
