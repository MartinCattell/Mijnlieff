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
        elif self.board_shape == 2:
            self.menu_image = tkinter.PhotoImage(file="Line.gif")
        elif self.board_shape == 3:
            self.menu_image = tkinter.PhotoImage(file="L.gif")
        elif self.board_shape == 4:
            self.menu_image = tkinter.PhotoImage(file="T.gif")
        elif self.board_shape == 5:
            self.menu_image = tkinter.PhotoImage(file="S.gif")
        self.shape_button = tkinter.Button(self.root, image=self.menu_image, font="verdana 10 bold",
                                           command=self.shape_changer)
        self.shape_button.grid(row=2, column=0)

    def start_game(self):
        game_window = tkinter.Toplevel(self.root)
        game_window.title("Mijnlieff")
        game_window.grab_set()

        game = Game(game_window, self.board_shape)
        game.board_frame.grid(row=0, column=0, columnspan=2)
        game.p1_tile_frame.grid(row=1, column=0)
        game.p2_tile_frame.grid(row=1, column=1)


class Game(object):
    def __init__(self, frame, board_shape):
        self.board_frame = tkinter.Frame(frame)
        self.board_frame.grid(row=1, column=0)
        self.p1_tile_frame = tkinter.Frame(frame, height=50)
        self.p1_tile_frame.grid(row=2, column=0)
        self.p2_tile_frame = tkinter.Frame(frame, height=50)
        self.p2_tile_frame.grid(row=2, column=1)

        self.board = Board(board_shape, self)
        self.board.board_edge.grid(row=0, column=0)

        self.p1_tile_list = [[Tile(1, 1, 0, self), Tile(2, 1, 0, self), Tile(3, 1, 0, self), Tile(4, 1, 0, self)],
                             [Tile(1, 1, 1, self), Tile(2, 1, 1, self), Tile(3, 1, 1, self),  Tile(4, 1, 1, self)]]

        self.p2_tile_list = [[Tile(1, 2, 0, self), Tile(2, 2, 0, self), Tile(3, 2, 0, self), Tile(4, 2, 0, self)],
                             [Tile(1, 2, 1, self), Tile(2, 2, 1, self), Tile(3, 2, 1, self),  Tile(4, 2, 1, self)]]

        self.p1_tile_list[0][0].label.grid(row=0, column=0)
        self.p1_tile_list[0][1].label.grid(row=0, column=1)
        self.p1_tile_list[0][2].label.grid(row=0, column=2)
        self.p1_tile_list[0][3].label.grid(row=0, column=3)
        self.p1_tile_list[1][0].label.grid(row=1, column=0)
        self.p1_tile_list[1][1].label.grid(row=1, column=1)
        self.p1_tile_list[1][2].label.grid(row=1, column=2)
        self.p1_tile_list[1][3].label.grid(row=1, column=3)
        self.p2_tile_list[0][0].label.grid(row=0, column=0)
        self.p2_tile_list[0][1].label.grid(row=0, column=1)
        self.p2_tile_list[0][2].label.grid(row=0, column=2)
        self.p2_tile_list[0][3].label.grid(row=0, column=3)
        self.p2_tile_list[1][0].label.grid(row=1, column=0)
        self.p2_tile_list[1][1].label.grid(row=1, column=1)
        self.p2_tile_list[1][2].label.grid(row=1, column=2)
        self.p2_tile_list[1][3].label.grid(row=1, column=3)

        self.tile_select = 0
        self.tile_row = 0
        self.player_turn = 1
        self.player_belongs = 0


class Board(object):
    def __init__(self, shape, game):
        self.game = game
        self.board_edge = tkinter.Frame(game.board_frame)
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
                b = BoardSquare(self, i, j, self.game)
                row_list.append(b)
                row_list[j-column_start].square.grid(row=i, column=j)
            self.board_list.append(row_list)

    def board_build1(self, rows, columns):
        for i in range(rows):
            row_list = []
            for j in range(columns):
                b = BoardSquare(self, i, j, self.game)
                row_list.append(b)
                row_list[j].square.grid(row=i, column=j)
            self.board_list.append(row_list)


class BoardSquare(object):
    def __init__(self, board, row, column, game):
        side = 19
        height = 9
        self.board = board
        self.game = game
        self.row = row
        self.column = column
        self.square = tkinter.Label(self.board.board_edge, height=height, width=side, relief="groove")
        self.active = True
        self.square.bind("<Button-1>", self.tile_placer)
        self.tiled = False

    def active_switch(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def tile_placer(self, event):
        straightp1_img = tkinter.PhotoImage(file="straightp1.gif")
        diagonalp1_img = tkinter.PhotoImage(file="diagonalp1.gif")
        pullerp1_img = tkinter.PhotoImage(file="pullerp1.gif")
        pusherp1_img = tkinter.PhotoImage(file="pusherp1.gif")
        straightp2_img = tkinter.PhotoImage(file="straightp2.gif")
        diagonalp2_img = tkinter.PhotoImage(file="diagonalp2.gif")
        pullerp2_img = tkinter.PhotoImage(file="pullerp2.gif")
        pusherp2_img = tkinter.PhotoImage(file="pusherp2.gif")
        if self.active:
            if self.game.tile_select == 0:
                pass
            elif self.game.player_turn == 1:
                self.tiled = True
                if self.game.tile_select == 1:
                    self.straight_changer()
                    self.tile_image_place(straightp1_img)
                elif self.game.tile_select == 2:
                    self.diag_changer()
                    self.tile_image_place(diagonalp1_img)
                elif self.game.tile_select == 3:
                    self.pull_changer()
                    self.tile_image_place(pullerp1_img)
                elif self.game.tile_select == 4:
                    self.push_changer()
                    self.tile_image_place(pusherp1_img)
                self.active = False
                self.game.player_turn = 2
            elif self.game.player_turn == 2:
                self.tiled = True
                if self.game.tile_select == 1:
                    self.straight_changer()
                    self.tile_image_place(straightp2_img)
                elif self.game.tile_select == 2:
                    self.diag_changer()
                    self.tile_image_place(diagonalp2_img)
                elif self.game.tile_select == 3:
                    self.pull_changer()
                    self.tile_image_place(pullerp2_img)
                elif self.game.tile_select == 4:
                    self.push_changer()
                    self.tile_image_place(pusherp2_img)
                self.active = False
                self.game.player_turn = 1
            self.game.tile_select = 0

    def reset_board(self):
        for row in self.game.board.board_list:
            for square in row:
                square.square.config(bg="SystemButtonFace")
                if not square.tiled:
                    square.active = True

    def straight_changer(self):
        self.reset_board()
        for row in self.game.board.board_list:
            for square in row:
                if not square.tiled:
                    if square.row == self.row or square.column == self.column:
                        square.square.config(bg="#B7DEB3")
                    else:
                        square.active = False
                        square.square.config(bg="#BF9696")


    def diag_changer(self):
        self.reset_board()
        for row in self.game.board.board_list:
            c_1 = self.column - self.row
            c_2 = self.column + self.row
            for square in row:
                if not square.tiled:
                    if square.column == square.row + c_1 or square.column == -square.row + c_2:
                        square.square.config(bg="#B7DEB3")
                    else:
                        square.active = False
                        square.square.config(bg="#BF9696")

    def pull_changer(self):
        self.reset_board()
        for row in self.board.board_list:
            for square in row:
                if not square.tiled:
                    if self.column - 1 <= square.column <= self.column+1 and self.row - 1 <= square.row <= self.row + 1:
                        square.square.config(bg="#B7DEB3")
                    else:
                        square.active = False
                        square.square.config(bg="#BF9696")

    def push_changer(self):
        self.reset_board()
        for row in self.game.board.board_list:
            for square in row:
                if not square.tiled:
                    if self.column - 1 <= square.column <= self.column+1 and self.row - 1 <= square.row <= self.row + 1:
                        square.square.config(bg="#BF9696")
                        square.active = False
                    else:
                        square.square.config(bg="#B7DEB3")

    def tile_image_place(self, image):
        self.square = tkinter.Label(self.board.board_edge, image=image)
        self.square.image = image
        self.square.grid(row=self.row, column=self.column)
        if self.game.player_turn == 1:
            tile_label = self.game.p1_tile_list[self.game.tile_row][self.game.tile_select-1].label
            tile_label.destroy()
            tile_label = tkinter.Frame(self.game.p1_tile_frame, height=104, width=104)
            tile_label.grid(row=self.game.tile_row, column=self.game.tile_select-1)

        elif self.game.player_turn == 2:
            tile_label = self.game.p2_tile_list[self.game.tile_row][self.game.tile_select-1].label
            tile_label.destroy()
            tile_label = tkinter.Frame(self.game.p2_tile_frame, height=104, width=104)
            tile_label.grid(row=self.game.tile_row, column=self.game.tile_select-1)


class Tile(object):
    def __init__(self, typ, p, row, game):
        straightp1_img = tkinter.PhotoImage(file="straightp1.gif")
        diagonalp1_img = tkinter.PhotoImage(file="diagonalp1.gif")
        pullerp1_img = tkinter.PhotoImage(file="pullerp1.gif")
        pusherp1_img = tkinter.PhotoImage(file="pusherp1.gif")
        straightp2_img = tkinter.PhotoImage(file="straightp2.gif")
        diagonalp2_img = tkinter.PhotoImage(file="diagonalp2.gif")
        pullerp2_img = tkinter.PhotoImage(file="pullerp2.gif")
        pusherp2_img = tkinter.PhotoImage(file="pusherp2.gif")
        self.game = game
        self.tile_window = None
        self.label = None
        self.player_belongs = p
        self.type = typ
        self.row = row
        if self.player_belongs == 1:
            if self.type == 1:
                self.tile_image(straightp1_img, self.game.p1_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 2:
                self.tile_image(diagonalp1_img, self.game.p1_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 3:
                self.tile_image(pullerp1_img, self.game.p1_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 4:
                self.tile_image(pusherp1_img, self.game.p1_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
        if self.player_belongs == 2:
            if self.type == 1:
                self.tile_image(straightp2_img, self.game.p2_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 2:
                self.tile_image(diagonalp2_img, self.game.p2_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 3:
                self.tile_image(pullerp2_img, self.game.p2_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)
            elif self.type == 4:
                self.tile_image(pusherp2_img, self.game.p2_tile_frame)
                self.label.bind("<Button-1>", self.tile_selector)

    def tile_image(self, image, frame):
        self.label = tkinter.Label(frame, image=image)
        self.label.image = image

    def tile_selector(self, event):
        if self.player_belongs == self.game.player_turn:
            self.game.tile_select = self.type
            self.game.tile_row = self.row
        else:
            self.game.tile_select = 0



main_window = MainWindow()
main_window.root.mainloop()
