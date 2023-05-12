from constants import *
import Piece, Field

class Queue:
    def __init__(self):
        pass

class Field:
    def __init__(self, field: Field.Field = None, width:int = BOARD_WIDTH, height:int = BOARD_HEIGHT, active: Piece.Piece = Piece()):
        self._width, self._height = width, height
        self._field = field
        self._active = active

    def copy(self) -> Field.Field:
        return Field(field = self._field, width = self._width, height = self._height, active = self._active.copy())

    def lock(self, next: Queue) -> None:
        pass
