from constants import *
import Piece

class Piece:
    def __init__(self, type:str = None, orientation:int = 0) -> None:
        assert type in "_IJLOSTZ█"
        self.type = type
        self.orientation = orientation

    def copy(self) -> Piece:
        pass