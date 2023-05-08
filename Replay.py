class Replay:
    def __init__(self) -> None:
        self.frames = []

class Replay_Frame:
    def __init__(self) -> None:
        self.field = None
        self.message = None 
        self.queue = None
        self.garbage_queue = None
        self.timestamp = 0