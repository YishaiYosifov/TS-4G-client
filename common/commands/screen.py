from common.util import blockScreen
import keyboard

def block_screen():
    keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
    keyboard.add_hotkey("alt+f4", lambda: None, suppress=True)
    blockScreen.start()

def unblock_screen():
    keyboard.remove_hotkey("alt+tab")
    keyboard.remove_hotkey("alt+f4")
    blockScreen.close()