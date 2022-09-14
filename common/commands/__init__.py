from .screen import *
from .input import *

commandFunctions = {}
def init_command_functions(commands : list):
    for command in commands: commandFunctions[command] = locals()[command]