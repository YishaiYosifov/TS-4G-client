import threading
import keyboard
import tkinter

def block_screen():
    keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
    keyboard.add_hotkey("alt+f4", lambda: None, suppress=True)
    blockScreen.start()

def unblock_screen():
    keyboard.remove_hotkey("alt+tab")
    keyboard.remove_hotkey("alt+f4")
    blockScreen.close()

class BlockScreen(threading.Thread):
    def __init__(self): threading.Thread.__init__(self)
    
    def close(self): self.root.quit()
    
    def run(self):
        self.root = tkinter.Tk()
        self.root.configure(background="black")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.mainloop()
blockScreen = BlockScreen()