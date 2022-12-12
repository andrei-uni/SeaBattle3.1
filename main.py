import platform
from functools import partial

from tkinter import *

from Cell import Cell
from ShipPlacementModel import ShipPlacementModel
from GameModel import GameModel
from RandomShipPlacement import RandomShipPlacement


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title("Морской бой")
        self.SCREEN_WIDTH = self.root.winfo_screenwidth()
        self.BUTTON_SIZE = self.SCREEN_WIDTH / 24

        self.my_button_field = None

        self.place_ships_buttons = None
        self.ships_left_to_place_labels = None

        self.rotate_ship_button = None
        self.remove_ship_button = None
        self.remove_all_ships_button = None
        self.start_game_button = None
        self.place_ships_randomly_button = None

        self.opponent_field = None

        self.ship_placement_model = ShipPlacementModel()
        self.game_model = None

        self.create_button_field()
        self.create_buttons()

    def create_button_field(self):
        self.my_button_field = [[None for _ in range(10)] for _ in range(10)]

        for row in range(10):
            for column in range(10):
                btn = Button(relief=GROOVE, command=partial(self.field_button_pressed, row, column))
                btn.place(x=column * self.BUTTON_SIZE, y=row * self.BUTTON_SIZE,
                          height=self.BUTTON_SIZE, width=self.BUTTON_SIZE)
                btn.bind("<Enter>", lambda event, r=row, c=column: self.on_enter(event, r, c))
                btn.bind("<Leave>", lambda event: self.on_leave(event))
                self.my_button_field[row][column] = btn

    def on_enter(self, e, row: int, column: int):
        self.ship_placement_model.hovering_over(row, column)
        self.update_ui()

    def on_leave(self, e):
        self.ship_placement_model.leaving()
        self.update_ui()

    def create_buttons(self):
        self.place_ships_buttons = [None for _ in range(4)]
        self.ships_left_to_place_labels = [None for _ in range(4)]

        width = 60
        height = 40
        vert_pad = 5
        hor_pad = 5

        place_rand_btn = Button(text="🎲 Случайная расстановка", relief=GROOVE, command=self.place_randomly_pressed)
        place_rand_btn.place(x=self.SCREEN_WIDTH / 2, height=height)
        self.place_ships_randomly_button = place_rand_btn

        for row in range(4):
            place_btn = Button(text=f"{row + 1} пал.", relief=GROOVE, command=partial(self.choose_ship_pressed, row))
            place_btn.place(x=self.SCREEN_WIDTH / 2, y=(row + 1) * height + (row + 1) * vert_pad, width=width, height=height)
            self.place_ships_buttons[row] = place_btn

            label = Label(text=self.ships_left_template(4 - row))
            label.place(x=self.SCREEN_WIDTH / 2 + width + hor_pad,
                        y=(row + 1) * height + (row + 1) * vert_pad, height=height)
            self.ships_left_to_place_labels[row] = label

        rotate_btn = Button(text="⭮ Повернуть", relief=RAISED, command=self.rotate_ship_pressed)
        rotate_btn.place(x=self.SCREEN_WIDTH / 2, y=5 * height + 4 * vert_pad, height=height)
        self.rotate_ship_button = rotate_btn

        remove_btn = Button(text="╳ Убрать", relief=RAISED, command=self.remove_ship_pressed)
        remove_btn.place(x=self.SCREEN_WIDTH / 2, y=6 * height + 5 * vert_pad, height=height)
        self.remove_ship_button = remove_btn

        remove_all_btn = Button(text="❌ Очистить", relief=GROOVE, command=self.remove_all_ships_pressed)
        remove_all_btn.place(x=self.SCREEN_WIDTH / 2, y=7 * height + 9 * vert_pad, height=height)
        self.remove_all_ships_button = remove_all_btn

        start_game_btn = Button(text="💣 Начать", relief=GROOVE, state=DISABLED, command=self.start_game)
        start_game_btn.place(x=self.SCREEN_WIDTH / 2, y=8 * height + 13 * vert_pad, height=height)
        self.start_game_button = start_game_btn

    def choose_ship_pressed(self, row: int):
        if self.ship_placement_model.is_remove_ship_mode:
            self.remove_ship_pressed()

        self.ship_placement_model.choose_ship(row)

    def rotate_ship_pressed(self):
        self.ship_placement_model.rotate_ship_toggle()
        self.rotate_ship_button.config(relief=SUNKEN if self.ship_placement_model.is_ship_rotated else RAISED)

    def remove_ship_pressed(self):
        self.ship_placement_model.remove_ship_mode_toggle()
        self.remove_ship_button.config(relief=SUNKEN if self.ship_placement_model.is_remove_ship_mode else RAISED)

    def remove_all_ships_pressed(self):
        self.ship_placement_model.remove_all_ships()
        self.update_ui()

    def place_randomly_pressed(self):
        self.ship_placement_model.place_ships_randomly()
        self.update_ui()

    def field_button_pressed(self, row: int, column: int):
        if self.ship_placement_model.is_remove_ship_mode:
            self.ship_placement_model.try_remove_ship(row, column)
        else:
            self.ship_placement_model.try_place_ship(row, column)

        self.update_ui()

    def update_ui(self):
        self.redraw_field()
        self.update_labels()
        self.update_start_button()

    def redraw_field(self):
        new_field = self.ship_placement_model.get_field()

        for row in range(10):
            for column in range(10):
                state = new_field[row][column].state
                self.my_button_field[row][column].config(bg=Cell.STATE_TO_COLOR[state])

    def update_labels(self):
        for i in range(4):
            self.ships_left_to_place_labels[i].config(
                text=self.ships_left_template(self.ship_placement_model.ships_left_for_type(i)))

    def update_start_button(self):
        self.start_game_button.config(state=ACTIVE if self.ship_placement_model.all_ships_placed() else DISABLED)

    def ships_left_template(self, count: int) -> str:
        return f"{count} осталось"

    def start_game(self):
        self.remove_ships_placement_widgets()
        self.disable_my_field()
        self.create_opponent_field()

        self.game_model = GameModel(self.ship_placement_model.field, RandomShipPlacement().place())

    def remove_ships_placement_widgets(self):
        for i in range(4):
            self.place_ships_buttons[i].place_forget()
            self.ships_left_to_place_labels[i].place_forget()

        self.rotate_ship_button.place_forget()
        self.remove_ship_button.place_forget()
        self.remove_all_ships_button.place_forget()
        self.start_game_button.place_forget()
        self.place_ships_randomly_button.place_forget()

    def disable_my_field(self):
        for row in range(10):
            for column in range(10):
                btn = Button(relief=GROOVE, state=DISABLED)
                btn.place(x=column * self.BUTTON_SIZE, y=row * self.BUTTON_SIZE,
                          height=self.BUTTON_SIZE, width=self.BUTTON_SIZE)
                self.my_button_field[row][column] = btn

        self.redraw_field()

    def change_opponent_field_state(self, state: Cell.POSSIBLE_STATES):
        for r in range(10):
            for c in range(10):
                self.opponent_field[r][c].config(state=state)

    def create_opponent_field(self):
        self.opponent_field = [[None for _ in range(10)] for _ in range(10)]
        start_location = self.SCREEN_WIDTH - 10 * self.BUTTON_SIZE

        for row in range(10):
            for column in range(10):
                btn = Button(relief=GROOVE, command=partial(self.opponent_field_button_pressed, row, column))
                btn.place(x=start_location + column * self.BUTTON_SIZE, y=row * self.BUTTON_SIZE,
                          height=self.BUTTON_SIZE, width=self.BUTTON_SIZE)
                self.opponent_field[row][column] = btn

    def opponent_field_button_pressed(self, row: int, column: int):
        new_field = self.game_model.make_shot(row, column)
        self.redraw_opponent_field(new_field)
        self.bot_make_moves()

    def bot_make_moves(self):
        while not self.game_model.is_player_turn:
            # self.change_opponent_field_state(DISABLED)
            self.game_model.bot_make_shot()
            self.redraw_field()
        # self.change_opponent_field_state(ACTIVE)

    def redraw_opponent_field(self, source_field):
        for r in range(10):
            for c in range(10):
                self.opponent_field[r][c].config(bg=Cell.STATE_TO_COLOR[source_field[r][c].state])

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    if platform.system() == "Windows":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

    Application().run()
