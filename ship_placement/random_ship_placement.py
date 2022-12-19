from random import randint, random

from cell import Cell


class RandomShipPlacement:
    def __init__(self):
        self.ships_to_place = [4, 3, 2, 1]
        self.field = [[Cell() for _ in range(10)] for _ in range(10)]
        self.extended_field = self.create_extended_field()

    def place(self) -> list[list[Cell]]:
        for t in reversed(self.ships_to_place):
            for _ in range(t):
                self.place_ship(4 - t)

        return self.field

    def create_extended_field(self) -> list[list[Cell]]:
        ext = [[Cell('SHIP_PART') for _ in range(14)],
               [Cell('SHIP_PART')] + [Cell() for _ in range(12)] + [Cell('SHIP_PART')]
               ]

        for r in range(10):
            row = [Cell('SHIP_PART'), Cell()]
            row += self.field[r].copy()
            row += [Cell(), Cell('SHIP_PART')]
            ext.append(row)

        ext.append([Cell('SHIP_PART')] + [Cell() for _ in range(12)] + [Cell('SHIP_PART')])
        ext.append([Cell('SHIP_PART') for _ in range(14)])

        return ext

    def place_ship(self, ship_type: int):
        while True:
            r_row = randint(0, 9)
            r_column = randint(0, 9)
            r_rotated = random() < 0.5

            broke = False

            for i in range(ship_type + 1):
                if self.is_ship_in_vicinity(r_row + i * (not r_rotated), r_column + i * r_rotated):
                    broke = True
                    break

            if broke:
                continue

            for i in range(ship_type + 1):
                self.field[r_row + i * (not r_rotated)][r_column + i * r_rotated].change_state('SHIP_PART')

            self.extended_field = self.create_extended_field()

            break

    def is_ship_in_vicinity(self, row: int, column: int) -> bool:
        adjusted_row = row + 2
        adjusted_column = column + 2

        for i in range(-1, 1 + 1):
            for j in range(-1, 1 + 1):
                if self.extended_field[adjusted_row + i][adjusted_column + j].state == 'SHIP_PART':
                    return True

        return False
