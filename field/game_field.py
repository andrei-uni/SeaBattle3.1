from cell import Cell
from coord import Coord


class GameField:
    def __init__(self, field: list[list[Cell]]):
        self.field = field

    def extended_field(self) -> list[list[Cell]]:
        ext = [[Cell() for _ in range(12)]]
        for r in self.field:
            row = r.copy()
            row.append(Cell())
            row.insert(0, Cell())
            ext.append(row)
        ext.append([Cell() for _ in range(12)])
        return ext

    def receive_shot(self, r: int, c: int) -> bool:
        cell_state = self.get_cell(r, c).state

        if cell_state in ['SHIP_HIT', 'SHIP_PARTLY_HIT', 'MISSED']:
            return True

        if cell_state == 'EMPTY':
            self.change_cell_state(r, c, 'MISSED')
            return False

        if cell_state == 'SHIP_PART':
            self.change_cell_state(r, c, 'SHIP_PARTLY_HIT')

            if self.is_ship_fully_hit(r, c):
                for coord in self.get_ship_parts_coords(r, c):
                    self.change_cell_state(coord.row, coord.column, 'SHIP_HIT')
                    self.grey_out_area_around(coord.row, coord.column)

            return True

        raise Exception()

    def is_ship_fully_hit(self, row: int, column: int) -> bool:
        for coord in self.get_ship_parts_coords(row, column):
            if self.get_cell(coord.row, coord.column).state != 'SHIP_PARTLY_HIT':
                return False
        return True

    def get_ship_parts_coords(self, row: int, column: int) -> list[Coord]:
        if self.get_cell(row, column).state in ['EMPTY', 'MISSED']:
            return []
        res = [Coord(row, column)]

        for row_dir in range(-1, 1 + 1):
            for col_dir in range(-1, 1 + 1):
                if abs(row_dir) + abs(col_dir) != 1:
                    continue
                for i in range(1, 3 + 1):
                    try:
                        cell = self.get_cell(row + i * row_dir, column + i * col_dir)
                    except:
                        break
                    if cell.state in ['EMPTY', 'MISSED']:
                        break
                    res.append(Coord(row + i * row_dir, column + i * col_dir))

        return res

    def grey_out_area_around(self, row: int, column: int):
        for i in range(-1, 1 + 1):
            for j in range(-1, 1 + 1):
                if not Cell.is_in_bounds(row + i, column + j):
                    continue
                if self.get_cell(row + i, column + j).state == 'EMPTY':
                    self.change_cell_state(row + i, column + j, 'MISSED')

    def create_visible_field(self) -> list[list[Cell]]:
        f = [[Cell() for _ in range(10)] for _ in range(10)]

        for row in range(10):
            for col in range(10):
                real_state = self.get_cell(row, col).state
                f[row][col].state = real_state if real_state in ['SHIP_HIT', 'SHIP_PARTLY_HIT', 'MISSED'] else 'EMPTY'

        return f

    def change_cell_state(self, row: int, column: int, state: Cell.POSSIBLE_STATES):
        self.field[row][column].change_state(state)

    def get_cell(self, row: int, column: int) -> Cell:
        if not Cell.is_in_bounds(row, column):
            raise Exception()
        return self.field[row][column]

    @staticmethod
    def convert_to_gamefield(string: str):
        field = [[Cell() for _ in range(10)] for _ in range(10)]
        for coord in string.split(";"):
            coords = coord.split(",")
            r = int(coords[0])
            c = int(coords[1])
            field[r][c].change_state("SHIP_PART")
        return GameField(field)
