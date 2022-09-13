import keyboard
import ctypes

def run():
    for key in range(150): keyboard.unblock_key(key)
    ctypes.windll.user32.BlockInput(False)