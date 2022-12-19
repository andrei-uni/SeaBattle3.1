from random import choice

from cell import Cell
from coord import Coord


class Bot:
    def __init__(self):
        pass

    def choose_coord(self, visible_field: list[list[Cell]]) -> Coord:
        weight = self.get_weight_map(visible_field)
        return choice(self.get_max_weight_cells(weight))

    def get_weight_map(self, visible_field: list[list[Cell]]) -> list[list[int]]:
        weight = [[1 for _ in range(10)] for _ in range(10)]

        for r in range(10):
            for c in range(10):
                coord_state = visible_field[r][c].state
                if coord_state == 'SHIP_PARTLY_HIT':
                    weight[r][c] = 0

                    if r - 1 >= 0:
                        if c - 1 >= 0:
                            weight[r - 1][c - 1] = 0
                        weight[r - 1][c] *= 50
                        if c + 1 < 10:
                            weight[r - 1][c + 1] = 0

                    if c - 1 >= 0:
                        weight[r][c - 1] *= 50
                    if c + 1 < 10:
                        weight[r][c + 1] *= 50

                    if r + 1 < 10:
                        if c - 1 >= 0:
                            weight[r + 1][c - 1] = 0
                        weight[r + 1][c] *= 50
                        if c + 1 < 10:
                            weight[r + 1][c + 1] = 0
                elif coord_state in ['MISSED', 'SHIP_HIT']:
                    weight[r][c] = 0

        return weight

    def get_max_weight_cells(self, weight: list[list[int]]) -> list[Coord]:
        weights = {}
        max_weight = 0
        for r in range(10):
            for c in range(10):
                if weight[r][c] > max_weight:
                    max_weight = weight[r][c]
                weights.setdefault(weight[r][c], []).append(Coord(r, c))

        return weights[max_weight]
