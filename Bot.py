from random import choice

from Cell import Cell
from Coord import Coord


class Bot:
    def __init__(self):
        self.last_hit_coord = None
        self.last_success_hit_coord = None

    def choose_coord(self, field: list[list[Cell]]):
        if self.last_hit_coord is None:
            return self._choose_random_coord(field)

        last_hit_coord_state = field[self.last_hit_coord.row][self.last_hit_coord.column].state

        if last_hit_coord_state == 'SHIP_HIT':
            self.last_success_hit_coord = None
            return self._choose_random_coord(field)
        elif last_hit_coord_state == 'SHIP_PARTLY_HIT':
            self.last_success_hit_coord = self.last_hit_coord
        else:
            return self._choose_random_coord(field)
    #
    #     self._get_possible_next_moves_coords(self.last_success_hit_coord, field)
    #     self.last_hit_coord = choice(self.pts)
    #     self.pts = []
    #     return self.last_hit_coord
    #
    # def _get_possible_next_moves_coords(self, last_hit_coord: Coord, field: list[list[Cell]]):
    #     if not Cell.is_in_bounds(last_hit_coord.row, last_hit_coord.row):
    #         return
    #
    #     self.try_find_ship_parts(last_hit_coord.row + 1, last_hit_coord.column, field)
    #     self.try_find_ship_parts(last_hit_coord.row - 1, last_hit_coord.column, field)
    #     self.try_find_ship_parts(last_hit_coord.row, last_hit_coord.column + 1, field)
    #     self.try_find_ship_parts(last_hit_coord.row, last_hit_coord.column - 1, field)
    #
    # pts = []
    #
    # def try_find_ship_parts(self, row: int, column: int, field: list[list[Cell]]):
    #     if not Cell.is_in_bounds(row, column):
    #         return
    #     print(row, column, field[row][column].state)
    #     if field[row][column].state == 'EMPTY':
    #         self.pts.append(Coord(row, column))
    #         print("ADDED")
    #     elif field[row][column].state == 'SHIP_PARTLY_HIT':
    #         self.try_find_ship_parts(row + 1, column, field)
    #         self.try_find_ship_parts(row - 1, column, field)
    #         self.try_find_ship_parts(row, column + 1, field)
    #         self.try_find_ship_parts(row, column - 1, field)
    #
    # def _find_empty_cells_around(self, coord: Coord, field: list[list[Cell]]) -> list[Coord]:
    #     res = []
    #
    #     for r in range(-1, 1 + 1):
    #         for c in range(-1, 1 + 1):
    #             adj_r = coord.row + r
    #             adj_c = coord.column + c
    #
    #             if abs(r) + abs(c) != 1 or not Cell.is_in_bounds(adj_r, adj_c):
    #                 continue
    #
    #             if field[adj_r][adj_c].state == 'EMPTY':
    #                 res.append(Coord(adj_r, adj_c))
    #
    #     return res

    def _choose_random_coord(self, field: list[list[Cell]]) -> Coord:
        random_coord = choice(self._find_empty_coords(field))
        self.last_hit_coord = random_coord
        return random_coord

    def _find_empty_coords(self, field: list[list[Cell]]) -> list[Coord]:
        res = []
        for r in range(10):
            for c in range(10):
                if field[r][c].state == 'EMPTY':
                    res.append(Coord(r, c))
        return res
