from .input import blockInput

import threading
import tkinter

def block_screen():
    blockInput.start()
    blockScreen.start()

def unblock_screen():
    blockInput.unblock()
    blockScreen.close()

class BlockScreen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.blocked = False
    
    def run(self):
        if self.blocked: return

        self.blocked = True
        
        self.root = tkinter.Tk()
        self.root.configure(background="black")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.mainloop()
    
    def close(self):
        self.blocked = False
        self.root.quit()

        threading.Thread.__init__(self)
blockScreen = BlockScreen()