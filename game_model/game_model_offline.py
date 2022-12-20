import time

from bot import Bot
from field.cell import Cell
from field.game_field import GameField
from game_model.game_model import GameModel


class GameModelOffline(GameModel):
    def __init__(self, my_field: GameField, opponent_field: GameField):
        super().__init__(my_field, opponent_field)
        self.bot = Bot()

    def make_shot(self, row: int, column: int, game_field: GameField = None) -> list[list[Cell]]:
        player_shoots = game_field is None
        if player_shoots:
            game_field = self.opponent_field

        did_hit_ship = game_field.receive_shot(row, column)
        self.is_player_turn = did_hit_ship if player_shoots else not did_hit_ship

        return game_field.create_visible_field()

    def opponent_make_shot(self):
        time.sleep(0.5)
        coord = self.bot.choose_coord(self.my_field.create_visible_field())
        self.make_shot(coord.row, coord.column, self.my_field)
