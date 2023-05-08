from constants import *
import Piece, Field

class Field:
    def __init__(self, field:Field = None, width:int = BOARD_WIDTH, height:int = BOARD_HEIGHT, active:Piece = Piece()):
        self.width, self.height = width, height
        self.field = field
        self.active = active

    def copy(self) -> Field:
        return Field(field = self.field, width = self.width, height = self.height, active = self.active.copy())

