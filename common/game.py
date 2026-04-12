from enum import Enum


class Type(str, Enum):
    TIC_TAC_TOE = 'tic_tac_toe'


class Result(str, Enum):
    TBD = 'tbd'
    DRAW = 'draw'
    P1_WON = 'p1_won'
    P2_WON = 'p2_won'


class Status(str, Enum):
    IN_QUEUE = 'in_queue'
    IN_PROGRESS = 'in_progress'
    ABANDONED = 'abandoned'
    FINISHED = 'finished'
