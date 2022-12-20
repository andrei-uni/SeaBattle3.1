from field.cell import Cell
from field.coord import Coord
from field.game_field import GameField
from game_model.game_model import GameModel
from networking.network import Network


class GameModelOnline(GameModel):
    def __init__(self, my_field: GameField, opponent_field: GameField, my_turn: bool, network: Network):
        super().__init__(my_field, opponent_field)
        self.is_player_turn = my_turn
        self.network = network

    def make_shot(self, row: int, column: int) -> list[list[Cell]]:
        did_hit_ship = self.opponent_field.receive_shot(row, column)

        self.network.send_move_coord(Coord(row, column))
        self.network.send_hit_ship(did_hit_ship)

        self.is_player_turn = did_hit_ship
        return self.opponent_field.create_visible_field()

    def opponent_make_shot(self):
        coord = self.network.receive_move_coord()
        self.is_player_turn = not self.my_field.receive_shot(coord.row, coord.column)
