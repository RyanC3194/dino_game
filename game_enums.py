from enum import Enum


class DinoState(Enum):
    GROUND = 0
    AIR_UP = 1
    AIR_DOWN = 2


class DinoActions(Enum):
    Nothing = None
    Jump = 1
