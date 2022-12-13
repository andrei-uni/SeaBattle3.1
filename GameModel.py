from Bot import Bot
from Cell import Cell
from GameField import GameField


class GameModel:
    _total_hit_cells_for_win = 4 + 2*3 + 3*2 + 4*1

    def __init__(self, my_field: list[list[Cell]], opponent_field: list[list[Cell]]):
        self.my_field = GameField(my_field)
        self.opponent_field = GameField(opponent_field)
        self.is_player_turn = True
        self.bot = Bot()

    def is_my_win(self) -> bool:
        return self._all_ships_hit(self.opponent_field)

    def is_opponent_win(self) -> bool:
        return self._all_ships_hit(self.my_field)

    def _all_ships_hit(self, game_field: GameField) -> bool:
        hit_count = 0
        for r in range(10):
            for c in range(10):
                cell_state = game_field.get_cell(r, c).state
                if cell_state == 'SHIP_HIT':
                    hit_count += 1

        return hit_count == self._total_hit_cells_for_win

    def make_shot(self, row: int, column: int, game_field: GameField = None) -> list[list[Cell]]:
        player_shoots = game_field is None
        if player_shoots:
            game_field = self.opponent_field

        did_hit_ship = game_field.receive_shot(row, column)
        self.is_player_turn = did_hit_ship if player_shoots else not did_hit_ship

        return game_field.create_visible_field()

    def bot_make_shot(self):
        coord = self.bot.choose_coord(self.my_field.create_visible_field())
        self.make_shot(coord.row, coord.column, self.my_field)
