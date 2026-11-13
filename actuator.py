import pyautogui
import time
import threading
import speech_recognition as sr

# PyAutoGUI Config
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

# Global Variables
screen_width, screen_height = pyautogui.size()
DELAY_TIME = 0.01
wrap_around = False
CURSOR_SPEED = 1  # Increased slightly to 2 so movement feels responsive
SCROLL_SPEED = 50
CMD = None  # Current command being implemented


def set_command(new_cmd):
    """Callback function triggered by speech_recognition.py"""
    global CMD
    CMD = new_cmd


def scroll_down():
    pyautogui.scroll(-SCROLL_SPEED)


def scroll_up():
    pyautogui.scroll(SCROLL_SPEED)


def double_click():
    pyautogui.doubleClick()


def right_click():
    pyautogui.rightClick()


def click():
    pyautogui.click()


def move_stop():
    time.sleep(DELAY_TIME)


def move_down():
    pyautogui.move(0, CURSOR_SPEED)
    time.sleep(DELAY_TIME)
    current_x, current_y = pyautogui.position()
    if current_y >= screen_height - 10 and wrap_around:
        pyautogui.moveTo(current_x, 10)


def move_up():
    pyautogui.move(0, -CURSOR_SPEED)
    time.sleep(DELAY_TIME)
    current_x, current_y = pyautogui.position()
    if current_y <= 10 and wrap_around:
        pyautogui.moveTo(current_x, screen_height - 10)


def move_left():
    pyautogui.move(-CURSOR_SPEED, 0)
    time.sleep(DELAY_TIME)
    current_x, current_y = pyautogui.position()
    if current_x <= 10 and wrap_around:
        pyautogui.moveTo(screen_width - 10, current_y)


def move_right():
    pyautogui.move(CURSOR_SPEED, 0)
    time.sleep(DELAY_TIME)
    current_x, current_y = pyautogui.position()
    if current_x >= screen_width - 10 and wrap_around:
        pyautogui.moveTo(10, current_y)


def move_cursor_loop():
    global CMD
    while True:
        # Continuous actions (keep running until changed)
        if CMD == "up":
            move_up()
        elif CMD == "down":
            move_down()
        elif CMD == "left":
            move_left()
        elif CMD == "right":
            move_right()
        elif CMD == "stop":
            move_stop()

        # One-off actions (execute once, then clear CMD so they don't repeat)
        elif CMD == "click":
            click()
            CMD = None
        elif CMD == "double click":
            double_click()
            CMD = None
        elif CMD == "right click":
            right_click()
            CMD = None
        elif CMD == "scroll up":
            scroll_up()
            CMD = None
        elif CMD == "scroll down":
            scroll_down()
            CMD = None

        time.sleep(0.001)


# 1. Start the background thread for cursor movement
threading.Thread(target=move_cursor_loop, daemon=True).start()

# 2. Start listening for speech and pass commands to set_command()
sr.speech_to_text(set_command)
