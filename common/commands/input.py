import threading
import keyboard
import ctypes
import time

def block_input(): blockInput.start()

def unblock_input(): blockInput.unblock()

class BlockInput(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.blocked = False

    def run(self):
        if self.blocked: return
        
        self.blocked = True

        for i in range(150): keyboard.block_key(i)
        while self.blocked:
            ctypes.windll.user32.BlockInput(True)
            time.sleep(1)
    
    def unblock(self):
        for i in range(150): keyboard.unblock_key(i)
        ctypes.windll.user32.BlockInput(False)
        self.blocked = False

        threading.Thread.__init__(self)

blockInput = BlockInput()