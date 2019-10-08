import tkinter
import keyboard
import time


class MainWindow(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Mijnlieff")
        self.new_game_button = tkinter.Button(self.root, text="Start Game", font="veranda 14 bold",
                                              command=self.start_game)
        self.new_game_button.grid(row=0, column=0)
        self.menu_image = tkinter.PhotoImage(file="Square.gif")
        self.shape_button = tkinter.Button(self.root, image=self.menu_image, font="verdana 10 bold",
                                           command=self.shape_changer)
        self.shape_button.grid(row=2, column=0)
        self.shape_label = tkinter.Label(self.root, text="Select a board shape", font="verdana 8")
        self.shape_label.grid(row=1, column=0)
        self.board_shape = 1

    def shape_changer(self):
        self.board_shape += 1
        if self.board_shape > 5:
            self.board_shape = 1
        if self.board_shape == 1:
            self.menu_image = tkinter.PhotoImage(file="Square.gif")
        if self.board_shape == 2:
            self.menu_image = tkinter.PhotoImage(file="Line.gif")
        if self.board_shape == 3:
            self.menu_image = tkinter.PhotoImage(file="L.gif")
        if self.board_shape == 4:
            self.menu_image = tkinter.PhotoImage(file="T.gif")
        if self.board_shape == 5:
            self.menu_image = tkinter.PhotoImage(file="S.gif")
        self.shape_button = tkinter.Button(self.root, image=self.menu_image, font="verdana 10 bold",
                                           command=self.shape_changer)
        self.shape_button.grid(row=2, column=0)

    def start_game(self):
        game_window = tkinter.Toplevel(self.root)
        game_window.title("Mijnlieff")
        game_window.grab_set()

        game = Game(game_window, self.board_shape)
        print(game.board.board_list)
        game.board_frame.grid(row=0, column=0, columnspan=2)
        game.p1_tile_frame.grid(row=1, column=0)
        game.p2_tile_frame.grid(row=1, column=1)


class Game(object):
    def __init__(self, frame, board_shape):
        self.board_frame = tkinter.Frame(frame)
        self.board_frame.grid(row=1, column=2, columnspan=2)
        self.p1_tile_frame = tkinter.Frame(frame, height=50)
        self.p1_tile_frame.grid(row=1, column=0)
        self.p2_tile_frame = tkinter.Frame(frame, height=50)
        self.p2_tile_frame.grid(row=1, column=4)

        self.board = Board(board_shape, self.board_frame)
        self.board.board_edge.grid(row=0, column=0)

        self.p1_tile_list = [Tile(1, 1, self.p1_tile_frame), Tile(1, 1, self.p1_tile_frame),
                             Tile(2, 1, self.p1_tile_frame), Tile(2, 1, self.p1_tile_frame),
                             Tile(3, 1, self.p1_tile_frame), Tile(3, 1, self.p1_tile_frame),
                             Tile(4, 1, self.p1_tile_frame), Tile(4, 1, self.p1_tile_frame)]
        self.p2_tile_list = [Tile(1, 2, self.p2_tile_frame), Tile(1, 2, self.p2_tile_frame),
                             Tile(2, 2, self.p2_tile_frame), Tile(2, 2, self.p2_tile_frame),
                             Tile(3, 2, self.p2_tile_frame), Tile(3, 2, self.p2_tile_frame),
                             Tile(4, 2, self.p2_tile_frame), Tile(4, 2, self.p2_tile_frame)]

        self.p1_tile_list[0].label.grid(row=0, column=0)
        self.p1_tile_list[1].label.grid(row=1, column=0)
        self.p1_tile_list[2].label.grid(row=0, column=1)
        self.p1_tile_list[3].label.grid(row=1, column=1)
        self.p1_tile_list[4].label.grid(row=0, column=2)
        self.p1_tile_list[5].label.grid(row=1, column=2)
        self.p1_tile_list[6].label.grid(row=0, column=3)
        self.p1_tile_list[7].label.grid(row=1, column=3)
        self.p2_tile_list[0].label.grid(row=0, column=0)
        self.p2_tile_list[1].label.grid(row=1, column=0)
        self.p2_tile_list[2].label.grid(row=0, column=1)
        self.p2_tile_list[3].label.grid(row=1, column=1)
        self.p2_tile_list[4].label.grid(row=0, column=2)
        self.p2_tile_list[5].label.grid(row=1, column=2)
        self.p2_tile_list[6].label.grid(row=0, column=3)
        self.p2_tile_list[7].label.grid(row=1, column=3)




class Board(object):
    def __init__(self, shape, window):
        self.board_edge = tkinter.Frame(window)
        self.board_list = []
        if shape == 1:
            self.board_build1(4, 4)

        elif shape == 2:
            self.board_build1(2, 8)

        elif shape == 3:
            self.board_build2(4, 0, 2, 1, 0, 6)

        elif shape == 4:
            self.board_build2(4, 2, 4, 1, 0, 6)

        elif shape == 5:
            self.board_build2(4, 2, 6, 1, 0, 4)

    def board_build2(self, rows, col_start1, col_end1, row_switch, col_start2, col_end2):
        for i in range(rows):
            column_start = col_start1
            column_end = col_end1
            row_list = []
            if i > row_switch:
                column_start = col_start2
                column_end = col_end2
            for j in range(column_start, column_end):
                b = BoardSquare(self.board_edge, i, j)
                row_list.append(b)
                row_list[j-column_start].square.grid(row=i, column=j)
            self.board_list.append(row_list)

    def board_build1(self, rows, columns):
        for i in range(rows):
            row_list = []
            for j in range(columns):
                b = BoardSquare(self.board_edge, i, j)
                row_list.append(b)
                row_list[j].square.grid(row=i, column=j)
            self.board_list.append(row_list)


class BoardSquare(object):
    def __init__(self, frame, row, column):
        side = 21
        height = 10
        self.row = row
        self.column = column
        self.square = tkinter.Label(frame, height=height, width=side, relief="groove")
        self.active = True

    def active_switch(self):
        if self.active:
            self.active = False
        else:
            self.active = True


class Tile(object):
    def __init__(self, typ, p, frame):
        straightp1_img = tkinter.PhotoImage(file="straightp1.gif")
        diagonalp1_img = tkinter.PhotoImage(file="diagonalp1.gif")
        pullerp1_img = tkinter.PhotoImage(file="pullerp1.gif")
        pusherp1_img = tkinter.PhotoImage(file="pusherp1.gif")
        straightp2_img = tkinter.PhotoImage(file="straightp2.gif")
        diagonalp2_img = tkinter.PhotoImage(file="diagonalp2.gif")
        pullerp2_img = tkinter.PhotoImage(file="pullerp2.gif")
        pusherp2_img = tkinter.PhotoImage(file="pusherp2.gif")
        self.label = None
        self.player = p
        self.type = typ
        if self.player == 1:
            if self.type == 1:
                self.tile_image(straightp1_img, frame)
            elif self.type == 2:
                self.tile_image(diagonalp1_img, frame)
            elif self.type == 3:
                self.tile_image(pullerp1_img, frame)
            elif self.type == 4:
                self.tile_image(pusherp1_img, frame)
        if p == 2:
            if self.type == 1:
                self.tile_image(straightp2_img, frame)
            elif self.type == 2:
                self.tile_image(diagonalp2_img, frame)
            elif self.type == 3:
                self.tile_image(pullerp2_img, frame)
            elif self.type == 4:
                self.tile_image(pusherp2_img, frame)

    def tile_image(self, image, frame):
        self.label = tkinter.Label(frame, image=image)
        self.label.image = image


main_window = MainWindow()
main_window.root.mainloop()
