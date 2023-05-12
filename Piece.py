from constants import *
import Piece

class Piece:
    def __init__(self, form:str = None, orientation:int = 0) -> None:
        assert form in " IJLOSTZ█"
        self._form = form
        self._orientation = orientation
        self._container = None

    def copy(self) -> Piece.Piece:
        pass
