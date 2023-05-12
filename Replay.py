import Field
import py_fumen

class Replay_Frame:
    def __init__(self) -> None:
        self._field = None
        self._message = None 
        self._queue = None
        self._garbage_queue = None
        self._root_time = None
        self._timestamp = None
    
    def set_field(self, field: Field.Field):
        pass

    def set_message(self, message: str):
        pass

    def set_queue(self, queue: Field.Queue):
        pass

    def set_garbage_queue(self, queue: list):
        pass

    def set_root_time(self, time: float):
        pass
    
    def set_time(self, time: float):
        pass

    def to_py_fumen(self) -> py_fumen.page.Page:
        pass

class Replay:
    def __init__(self) -> None:
        self._frames = []

    def add_frame(self, frame: Replay_Frame) -> None:
        pass

    def get_frame(self, index: int) -> Replay_Frame:
        pass

    def reset(self) -> None:
        pass

    def to_py_fumen(self) -> list:
        pass 
