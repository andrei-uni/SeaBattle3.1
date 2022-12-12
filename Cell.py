from typing import Literal


class Cell:
    POSSIBLE_STATES = Literal['EMPTY', 'SHIP_PART', 'CAN_PLACE', 'CANT_PLACE', 'SHIP_HIT', 'SHIP_PARTLY_HIT', 'MISSED']

    STATE_TO_COLOR = {
        'EMPTY':           'SystemButtonFace',
        'SHIP_PART':       'blue',
        'CAN_PLACE':       'cyan',
        'CANT_PLACE':      'red',
        'SHIP_HIT':        'red',
        'SHIP_PARTLY_HIT': 'red',
        'MISSED':          'grey62'
    }

    def __init__(self, state: POSSIBLE_STATES = 'EMPTY'):
        self.state = state

    def change_state(self, state: POSSIBLE_STATES):
        self.state = state

    @staticmethod
    def is_in_bounds(row: int, column: int) -> bool:
        if row < 0 or row > 9 or column < 0 or column > 9:
            return False
        return True
