import tkinter
import keyboard
import time


class MainWindow(object):
    root = tkinter.Tk()
    root.title("Mijnlieff")
    options_frame = tkinter.Frame(root)
    options_frame.grid(row=0, column=0, columnspan=2)
    new_game_button = tkinter.Button(options_frame, text="New Game")
    new_game_button.grid(row=0, column=0)
    restart_game_button = tkinter.Button(options_frame, text="Restart")
    restart_game_button.grid(row=0, column=1)
    options_button = tkinter.Button(options_frame, text="Options")
    options_button.grid(row=0, column=2)
    quit_game_button = tkinter.Button(options_frame, text="Quit")
    quit_game_button.grid(row=0, column=3)
    game_frame = tkinter.Frame(root, height=50, bg="blue")
    game_frame.grid(row=1, column=0, columnspan=2)
    p1_tile_frame = tkinter.Frame(root, height=50, bg="green")
    p1_tile_frame.grid(row=2, column=0)
    p2_tile_frame = tkinter.Frame(root, height=50, bg="red")
    p2_tile_frame.grid(row=2, column=1)
    root.mainloop()

    def __init__(self):
        self.board = None


class Game(object):
    def __init__(self):
        pass
    pass


class Board(object):
    def __init__(self, shape):
        self.shape = shape

    pass


class Tile(object):
    def __init__(self, type):
        self.type = type
    pass




