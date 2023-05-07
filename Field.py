from constants import *

class Field:
    def __init__(self, input = None, width = BOARD_WIDTH, height =  BOARD_HEIGHT):
        self.field = input if input else bytearray(width*height)