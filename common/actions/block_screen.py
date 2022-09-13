from common.util import blockScreen

import keyboard

def run():
    keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
    keyboard.add_hotkey("alt+f4", lambda: None, suppress=True)
    blockScreen.start()