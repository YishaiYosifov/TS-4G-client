from common.util import blockScreen
import keyboard

def run():
    keyboard.remove_hotkey("alt+tab")
    keyboard.remove_hotkey("alt+f4")
    blockScreen.close()