from field.game_field import GameField


class GameModel:
    _TOTAL_HIT_CELLS_FOR_WIN = 1 * 4 + 2 * 3 + 3 * 2 + 4 * 1

    def __init__(self, my_field: GameField, opponent_field: GameField):
        self.my_field = my_field
        self.opponent_field = opponent_field
        self.is_player_turn = True

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

        return hit_count == self._TOTAL_HIT_CELLS_FOR_WIN
