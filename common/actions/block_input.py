import keyboard
import ctypes

def run():
    for key in range(150): keyboard.block_key(key)
    ctypes.windll.user32.BlockInput(True)