# -*- coding: utf-8 -*-

from dataclasses import dataclass
from math import floor
from typing import Tuple

from .defines import is_mino_piece, InnerOperation, Piece, Rotation

@dataclass
class Action():
    piece: InnerOperation
    rise: bool
    mirror: bool
    colorize: bool
    comment: bool
    lock: bool

def decode_bool(n: int):
    return n != 0

class ActionDecoder() :
    width: int
    field_top: int
    garbage_line: int
    field_max_height: int
    num_field_blocks: int

    def __init__(self, width: int, field_top: int, garbage_line: int):
        self.width = width
        self.field_top = field_top
        self.garbage_line = garbage_line
        self.field_max_height = field_top + garbage_line
        self.num_field_blocks = self.field_max_height * width

    class PieceException(Exception):
        pass

    class RotationException(Exception):
        pass

    @staticmethod
    def decode_piece(n: int) -> Piece:
        if n in range(0, 9):
            return Piece(n)

        raise ActionDecoder.PieceException(f'Unexpected piece: {n} (0~8)')

    @staticmethod
    def decode_rotation(n: int) -> Rotation:
        if n in range(0, 4):
            return Rotation(n)

        raise ActionDecoder.RotationException(f'Unexpected rotation: {n} (0~3)')

    def decode_coordinate(self, n: int, piece: Piece, rotation: Rotation) -> Tuple[int, int]:
        x = n % self.width
        ORIGIN_Y = floor(n / 10)
        y = self.field_top - ORIGIN_Y - 1

        if piece is Piece.O and rotation is Rotation.LEFT:
            x += 1
            y -= 1
        elif piece is Piece.O and rotation is Rotation.REVERSE:
            x += 1
        elif piece is Piece.O and rotation is Rotation.SPAWN:
            y -= 1
        elif piece is Piece.I and rotation is Rotation.REVERSE:
            x += 1
        elif piece is Piece.I and rotation is Rotation.LEFT:
            y -= 1
        elif piece is Piece.S and rotation is Rotation.SPAWN:
            y -= 1
        elif piece is Piece.S and rotation is Rotation.RIGHT:
            x -= 1
        elif piece is Piece.Z and rotation is Rotation.SPAWN:
            y -= 1
        elif piece is Piece.Z and rotation is Rotation.LEFT:
            x += 1

        return (x, y)

    def decode(self, v: int) -> Action:
        value = v
        piece_type = self.decode_piece(value % 8)
        value = floor(value / 8)
        rotation = self.decode_rotation(value % 4)
        value = floor(value / 4)
        coordinate = self.decode_coordinate(value % self.num_field_blocks, piece_type, rotation)
        value = floor(value / self.num_field_blocks)
        is_block_up = decode_bool(value % 2)
        value = floor(value / 2)
        is_mirror = decode_bool(value % 2)
        value = floor(value / 2)
        is_color = decode_bool(value % 2)
        value = floor(value / 2)
        is_comment = decode_bool(value % 2)
        value = floor(value / 2)
        is_lock = not decode_bool(value % 2)

        return Action(
            piece = InnerOperation(
                x = coordinate[0],
                y = coordinate[1],
                piece_type = piece_type,
                rotation = rotation
                ),
            rise = is_block_up,
            mirror = is_mirror,
            colorize = is_color,
            comment = is_comment,
            lock = is_lock) 

def encode_bool(flag: bool) -> int:
    return 1 if flag else 0

class ActionEncoder():
    width: int
    field_top: int
    garbage_line: int
    field_max_height: int
    num_field_blocks: int

    def __init__(self, width: int, field_top: int, garbage_line: int):
        self.width = width
        self.field_top = field_top
        self.garbage_line = garbage_line
        self.field_max_height = field_top + garbage_line
        self.num_field_blocks = self.field_max_height * width

    def encode_position(self, operation: InnerOperation) -> int:
        piece_type = operation.piece_type
        rotation = operation.rotation
        x = operation.x
        y = operation.y

        if not is_mino_piece(piece_type):
            x = 0
            y = 22
        elif piece_type is Piece.O and rotation is Rotation.LEFT:
            x -= 1
            y += 1
        elif piece_type is Piece.O and rotation is Rotation.REVERSE:
            x -= 1
        elif piece_type is Piece.O and rotation is Rotation.SPAWN:
            y += 1
        elif piece_type is Piece.I and rotation is Rotation.REVERSE:
            x -= 1
        elif piece_type is Piece.I and rotation is Rotation.LEFT:
            y += 1
        elif piece_type is Piece.S and rotation is Rotation.SPAWN:
            y += 1
        elif piece_type is Piece.S and rotation is Rotation.RIGHT:
            x += 1
        elif piece_type is Piece.Z and rotation is Rotation.SPAWN:
            y += 1
        elif piece_type is Piece.Z and rotation is Rotation.LEFT:
            x -= 1

        return (self.field_top - y - 1) * self.width + x

    class NonReachableException(Exception):
        pass

    @staticmethod
    def encode_rotation(operation: InnerOperation) -> int:
        if not is_mino_piece(operation.piece_type):
            return 0

        if isinstance(operation.rotation, Rotation):
            return operation.rotation.value

        raise ActionEncoder.NonReachableException('No reachable rotation')

    def encode(self, action: Action) -> int:
        value = encode_bool(not action.lock)
        value *= 2
        value += encode_bool(action.comment)
        value *= 2
        value += encode_bool(action.colorize)
        value *= 2
        value += encode_bool(action.mirror)
        value *= 2
        value += encode_bool(action.rise)
        value *= self.num_field_blocks
        value += self.encode_position(action.piece)
        value *= 4
        value += self.encode_rotation(action.piece)
        value *= 8
        value += action.piece.piece_type.value

        return value