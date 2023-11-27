# main_script.py

import os
from PIL import Image
import pyautogui
from capture.capture import take_screenshot, save_screenshot
from image_processing.image_processing import create_step

def main():
    guide_folder = "output"
    os.makedirs(guide_folder, exist_ok=True)
    
    step_counter = 1
    steps = []

    while True:
        user_input = input(f"Press Enter to capture step {step_counter} (or any other key to end): ")

        if user_input != "":
            print("Ending the loop.")
            break  # Break out of the loop if the user enters any key other than Enter

        screenshot = take_screenshot()
        caption = input(f"Enter a caption for step {step_counter}: ")

        # Save the screenshot
        filename = f"{guide_folder}/step_{step_counter}.png"
        save_screenshot(screenshot, filename)

        # Create step with caption
        image = Image.open(filename)
        image_with_caption = create_step(image, caption)
        image_with_caption.save(filename)

        print(f"Step {step_counter} captured and saved as {filename}")

        # Append the image to the list of steps
        steps.append(image_with_caption)

        step_counter += 1

    # Combine all steps into a single image
    combined_image = Image.new("RGB", (steps[0].width, sum(img.height for img in steps)))
    y_offset = 0
    for step in steps:
        combined_image.paste(step, (0, y_offset))
        y_offset += step.height

    # Save the final combined image
    combined_filename = f"{guide_folder}/combined_steps.png"
    combined_image.save(combined_filename)
    print(f"Combined steps saved as {combined_filename}")

    # Show a confirmation dialog
    pyautogui.confirm("Screenshots captured. Press OK to exit.", title="Capture Complete")

if __name__ == "__main__":
    main()
