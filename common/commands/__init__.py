from .screenshare import *
from .screen import *
from .input import *
from .url import *

commandFunctions = {}
def init_command_functions(commands : list):
    for command in commands:
        command = command.lower()
        commandFunctions[command] = globals()[command]