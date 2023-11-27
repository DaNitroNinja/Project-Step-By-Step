import os
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw, ImageFont
from tkinter import simpledialog, messagebox

class ScreenshotButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, text="Capture Screenshot", command=self.capture_screenshot, **kwargs)
        self.steps = []  # List to store captured steps
        self.image_label = None  # Label to display the combined image

    def capture_screenshot(self):
        # Hide the main window temporarily
        self.master.iconify()

        # Capture the entire screen
        screenshot = ImageGrab.grab()

        # Ask the user for a caption using simpledialog
        caption = simpledialog.askstring("Caption", "Enter a caption for this step:")

        if caption is not None:  # Handle Cancel button in the dialog
            # Save the screenshot to the output folder
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            filename = os.path.join(output_folder, f"step_{len(self.steps) + 1}.png")
            screenshot.save(filename)

            # Create step with caption
            image = Image.open(filename)
            image_with_caption = self.add_caption(image, f"{len(self.steps) + 1}. {caption}")
            image_with_caption.save(filename)

            print(f"Step {len(self.steps) + 1} captured and saved as {filename} with caption: {caption}")

            # Append the image to the list of steps
            self.steps.append((image_with_caption, f"{len(self.steps) + 1}. {caption}"))
            self.show_current_step()  # Display the current step in the GUI
        else:
            print("Screenshot capture canceled.")

        # Show the main window again
        self.master.deiconify()

    def add_caption(self, image, caption):
        # Create a new image with the caption overlay
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Draw the caption on the new image
        draw.text((0, image.height - 20), caption, font=font, fill=(255, 255, 255, 255))

        return image

    def show_current_step(self):
        # Calculate the maximum width required for captions
        max_caption_width = max(len(step[1]) for step in self.steps) * 10  # Assuming 10 pixels per character

        # Calculate the height of the combined image
        combined_height = self.steps[0][0].height + 20  # Extra space for captions

        # Create a new image with the appropriate width and height
        combined_width = sum(step[0].width for step in self.steps) + max_caption_width
        combined_image = Image.new("RGB", (combined_width, combined_height), (255, 255, 255))

        # Paste each step and its caption onto the combined image
        x_offset = 0
        draw = ImageDraw.Draw(combined_image)
        font = ImageFont.load_default()

        for step, caption in self.steps:
            # Draw the step onto the combined image
            combined_image.paste(step, (x_offset, 0))

            # Draw caption below the step
            text_width, text_height = draw.textbbox((x_offset, 0, x_offset + step.width, 20), caption, font=font)[:2]
            text_position = (x_offset, 0)
            draw.rectangle([text_position, (x_offset + step.width, 20)], fill=(255, 255, 255))
            draw.text((x_offset, 0), caption, font=font, fill=(0, 0, 0))

            x_offset += step.width

        # Convert the combined image to Tkinter PhotoImage for display
        tk_image = ImageTk.PhotoImage(combined_image)

        # Display the image in a Tkinter label
        if self.image_label is not None:
            self.image_label.destroy()  # Remove the previous label

        self.image_label = tk.Label(self.master, image=tk_image)
        self.image_label.photo = tk_image  # Prevent the image from being garbage-collected
        self.image_label.pack()

    def quit_application(self):
        # Ask the user if they want to save the combined image
        if messagebox.askyesno("Save Combined Image", "Do you want to save the combined image before quitting?"):
            # Save the final combined image to the output folder
            combined_filename = os.path.join("output", "combined_steps.png")
            combined_image = self.combine_steps()
            combined_image.save(combined_filename)
            print(f"Combined steps saved as {combined_filename}")

        # Explicitly delete the PhotoImage object to avoid the warning
        self.image_label.photo = None

        self.master.destroy()  # Close the main window

    def combine_steps(self):
        # Combine all steps into a single image
        max_caption_width = max(len(step[1]) for step in self.steps) * 10  # Assuming 10 pixels per character
        combined_width = sum(step[0].width for step in self.steps) + max_caption_width  # Width of the combined image
        combined_height = self.steps[0][0].height + 20  # Extra space for captions

        combined_image = Image.new("RGB", (combined_width, combined_height), (255, 255, 255))
        draw = ImageDraw.Draw(combined_image)
        font = ImageFont.load_default()

        x_offset = 0
        for step, caption in self.steps:
            combined_image.paste(step, (x_offset, 0))

            # Draw caption below the step
            text_width, text_height = draw.textbbox((x_offset, 0, x_offset + step.width, 20), caption, font=font)[:2]
            text_position = (x_offset, 0)
            draw.rectangle([text_position, (x_offset + step.width, 20)], fill=(255, 255, 255))
            draw.text((x_offset, 0), caption, font=font, fill=(0, 0, 0))

            x_offset += step.width

        return combined_image

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
