import keyboard
import ctypes

def block_input():
    for key in range(150): keyboard.block_key(key)
    ctypes.windll.user32.BlockInput(True)

def unblock_input():
    for key in range(150): keyboard.unblock_key(key)
    ctypes.windll.user32.BlockInput(False)