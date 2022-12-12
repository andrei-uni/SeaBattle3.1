from Bot import Bot
from Cell import Cell
from GameField import GameField


class GameModel:
    def __init__(self, my_field, opponent_field):
        self.my_field = GameField(my_field)
        self.opponent_field = GameField(opponent_field)
        self.is_player_turn = True
        self.bot = Bot()

    def make_shot(self, row: int, column: int, game_field: GameField = None) -> list[list[Cell]]:
        player_shots = game_field is None
        if player_shots:
            game_field = self.opponent_field

        did_hit_ship = game_field.receive_shot(row, column)
        self.is_player_turn = did_hit_ship if player_shots else not did_hit_ship

        return game_field.create_visible_field()

    def bot_make_shot(self):
        coord = self.bot.choose_coord(self.my_field.create_visible_field())
        self.make_shot(coord.row, coord.column, self.my_field)
