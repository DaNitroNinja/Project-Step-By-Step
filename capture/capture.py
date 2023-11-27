#to take screenshots
import pyautogui
from PIL import Image

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

def save_screenshot(screenshot, filename):
    screenshot.save(filename)
