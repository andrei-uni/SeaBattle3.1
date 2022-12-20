from copy import deepcopy

from field.cell import Cell
from field.game_field import GameField
from ship_placement.random_ship_placement import RandomShipPlacement


class ShipPlacementModel:
    def __init__(self):
        self.current_ships_placed = [0, 0, 0, 0]

        self.previous_field = None
        self.field = [[Cell() for _ in range(10)] for _ in range(10)]

        self.current_ship_type = 3
        self.is_ship_rotated = False
        self.can_place = None
        self.is_remove_ship_mode = False

    def hovering_over(self, row: int, column: int):
        if self.is_remove_ship_mode:
            return

        self.previous_field = deepcopy(self.field)

        count = 0

        for i in range(self.current_ship_type + 1):
            if (self.is_ship_rotated and column + i == 10) or (not self.is_ship_rotated and row + i == 10):
                break

            row_offset = i if not self.is_ship_rotated else 0
            column_offset = i if self.is_ship_rotated else 0

            if self.is_ship_nearby(row + row_offset, column + column_offset) or \
                    self.current_ships_placed[self.current_ship_type] == 4 - self.current_ship_type:
                state = 'CANT_PLACE'
            else:
                state = 'CAN_PLACE'
                count += 1

            self.field[row + row_offset][column + column_offset].state = state

        self.can_place = count == self.current_ship_type + 1

    def leaving(self):
        if self.is_remove_ship_mode:
            return

        self.field = deepcopy(self.previous_field)

    def is_ship_nearby(self, row: int, column: int) -> bool:
        temp_field = self.create_temp_field()
        adjusted_row = row + 1
        adjusted_column = column + 1

        for i in range(-1, 1 + 1):
            for j in range(-1, 1 + 1):
                if temp_field[adjusted_row + j][adjusted_column + i].state == 'SHIP_PART':
                    return True

        return False

    def create_temp_field(self) -> list[list[Cell]]:
        temp_field = [[Cell() for _ in range(12)]]
        for r in self.field:
            row = r.copy()
            row.append(Cell())
            row.insert(0, Cell())
            temp_field.append(row)
        temp_field.append([Cell() for _ in range(12)])
        return temp_field

    def try_place_ship(self, row: int, column: int):
        if not self.can_place:
            return

        for i in range(self.current_ship_type + 1):
            self.field[row + i * (not self.is_ship_rotated)][column + i * self.is_ship_rotated].change_state(
                'SHIP_PART')

        self.current_ships_placed[self.current_ship_type] += 1

        self.previous_field = deepcopy(self.field)

    def try_remove_ship(self, row: int, column: int):
        self.try_remove_ship_part(row, column)
        if self._removed_parts == 0:
            return

        self.current_ships_placed[self._removed_parts - 1] -= 1
        self._removed_parts = 0

    _removed_parts = 0

    def try_remove_ship_part(self, row: int, column: int):
        if not Cell.is_in_bounds(row, column) or self.field[row][column].state != 'SHIP_PART':
            return

        self.field[row][column].change_state('EMPTY')
        self._removed_parts += 1

        self.try_remove_ship_part(row + 1, column)
        self.try_remove_ship_part(row - 1, column)
        self.try_remove_ship_part(row, column + 1)
        self.try_remove_ship_part(row, column - 1)

    def remove_all_ships(self):
        self.current_ships_placed = [0, 0, 0, 0]

        for row in range(10):
            for column in range(10):
                self.field[row][column].change_state('EMPTY')

    def remove_ship_mode_toggle(self):
        self.is_remove_ship_mode = not self.is_remove_ship_mode

    def rotate_ship_toggle(self):
        self.is_ship_rotated = not self.is_ship_rotated

    def choose_ship(self, ship_type: int):
        self.current_ship_type = ship_type

    def place_ships_randomly(self):
        self.field = RandomShipPlacement().place()
        self.current_ships_placed = [4, 3, 2, 1]

    def all_ships_placed(self) -> bool:
        for i in range(4):
            if not (self.current_ships_placed[i] == 4 - i):
                return False
        return True

    def ships_left_for_type(self, ship_type: int) -> int:
        return 4 - ship_type - self.current_ships_placed[ship_type]

    def get_field(self) -> list[list[Cell]]:
        return self.field

    def to_string(self) -> str:
        coords = []
        for r in range(10):
            for c in range(10):
                cell = self.field[r][c]
                if cell.state == 'SHIP_PART':
                    coords.append(f"{r},{c}")
        return ";".join(coords)

    def to_gamefield(self) -> GameField:
        return GameField(self.field)
