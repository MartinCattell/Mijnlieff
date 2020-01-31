import tkinter


class MainWindow(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.config(bg="#D4BFA8")
        self.root.title("Mijnlieff")
        self.root.resizable(0, 0)
        self.mijlieff = tkinter.Label(self.root, text="Mijnlieff", font=("gothic", 24, "bold"), bg="#D4BFA8").grid(row=0, column=0)
        self.new_game_button = tkinter.Button(self.root, text="Start Game", font="msserif 14",
                                              command=self.start_game, bg="#A18B73")
        self.new_game_button.grid(row=3, column=0)
        self.menu_image = tkinter.PhotoImage(file="Square.gif")
        self.shape_button = tkinter.Button(self.root, image=self.menu_image, font="msserif 10",
                                           command=self.shape_changer)
        self.shape_button.grid(row=2, column=0)
        self.shape_label = tkinter.Label(self.root, text="Select a board shape", font="msserif 8", bg="#D4BFA8")
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
        game_window = tkinter.Toplevel( bg="#D4BFA8")
        game_window.title("Mijnlieff")
        game_window.resizable(0,0)
        game_window.grab_set()

        game = Game(game_window, self.board_shape)


class Game(object):
    def __init__(self, frame, board_shape):
        self.frame = frame
        self.player_turn = 1    # -1 for player 2, 1 for player 1
        self.turn = 0

        self.p1_message = tkinter.Label(self.frame, text="Player 1\n Place your tile",
                                        font="none 20 bold", anchor="w", bg="#D4BFA8")
        self.p2_message = tkinter.Label(self.frame, text="Player 2\n Place your tile",
                                        font="none 20 bold", anchor="e", bg="#D4BFA8")
        self.player_messenger()
        if board_shape > 1:
            self.board_frame = tkinter.Frame(self.frame, bg="#D4BFA8")
            self.board_frame.grid(row=1, column=1, columnspan=2)
            self.p1_tile_frame = tkinter.Frame(self.frame)
            self.p1_tile_frame.grid(row=2, column=1, sticky="w")
            self.p2_tile_frame = tkinter.Frame(self.frame)
            self.p2_tile_frame.grid(row=2, column=2, sticky="e")
        else:
            self.board_frame = tkinter.Frame(self.frame, bg="#A6A599")
            self.board_frame.grid(row=1, column=1, columnspan=2)
            self.p1_tile_frame = tkinter.Frame(self.frame)
            self.p1_tile_frame.grid(row=2, column=0, sticky="w")
            self.p2_tile_frame = tkinter.Frame(self.frame)
            self.p2_tile_frame.grid(row=2, column=3, sticky="e")

        self.board = Board(self, board_shape)

        self.p1_tile_set = TileSet(self, 1)
        self.p2_tile_set = TileSet(self, -1)

        self.tile_select = 0
        self.tile_row = 0
        self.player_belongs = 0

        self.p1_tiles_placed = []
        self.p2_tiles_placed = []
        self.p1_tiles_remaining = 8
        self.p2_tiles_remaining = 8
        self.p1_lines_list = []
        self.p2_lines_list = []
        self.p1_score = 0
        self.p2_score = 0
        self.p1_score_label = tkinter.Label(self.frame, text="Player 1 score: " + str(self.p1_score), width=40, bg="#A9977A")
        self.p2_score_label = tkinter.Label(self.frame, text="Player 2 score: " + str(self.p2_score), width=40, bg="#A9977A")
        self.p1_score_label.grid(row=0, column=0, sticky="w")
        self.p2_score_label.grid(row=0, column=3, sticky="e")

    def line_checker(self, placed_list, lines_list):
        if self.turn >= 5:
            placed_list.sort()
            straight_master1 = []
            straight_master2 = []
            diagonal_master1 = []
            diagonal_master2 = []
            for a1 in placed_list:
                c_1 = a1[1] - a1[0]
                c_2 = a1[1] + a1[0]
                straight_list1 = [a1]
                straight_list2 = [a1]
                diagonal_list1 = [a1]
                diagonal_list2 = [a1]
                for a2 in placed_list:
                    if a2[0] == a1[0] and a2 not in straight_list1:
                        straight_list1.append(a2)
                    elif a2[1] == a1[1] and a2 not in straight_list2:
                        straight_list2.append(a2)
                    elif a2[1] == a2[0] + c_1 and a2 not in diagonal_list1:
                        diagonal_list1.append(a2)
                    elif a2[1] == -a2[0] + c_2 and a2 not in diagonal_list2:
                        diagonal_list2.append(a2)
                if len(straight_list1) > 2:
                    straight_list1.sort()
                    if straight_list1 not in straight_master1:
                        straight_master1.append(straight_list1)
                if len(straight_list2) > 2:
                    straight_list2.sort()
                    if straight_list2 not in straight_master2:
                        straight_master2.append(straight_list2)
                if len(diagonal_list1) > 2:
                    diagonal_list1.sort()
                    if diagonal_list1 not in diagonal_master1:
                        diagonal_master1.append(diagonal_list1)
                if len(diagonal_list2) > 2:
                    diagonal_list2.sort()
                    if diagonal_list2 not in diagonal_master2:
                        diagonal_master2.append(diagonal_list2)
            print(straight_master1)
            print(straight_master2)
            print(diagonal_master1)
            print(diagonal_master2)
            for line in straight_master1:
                for n in range(1, len(line)-1):
                    if line[n+1][1] == line[n][1] + 1 and line[n][1] == line[n-1][1] + 1:
                        new_line = [line[n-1], line[n], line[n+1]]
                        if new_line not in lines_list:
                            lines_list.append(new_line)
                            if self.player_turn == 1:
                                self.p1_score += 1
                                self.p1_score_label.config(text="Player 1 score: " + str(self.p1_score))
                            else:
                                self.p2_score += 1
                                self.p2_score_label.config(text="Player 2 score: " + str(self.p2_score))
            for line in straight_master2:
                for n in range(1, len(line)-1):
                    if line[n+1][0] == line[n][0] + 1 and line[n][0] == line[n-1][0] + 1:
                        new_line = [line[n-1], line[n], line[n+1]]
                        if new_line not in lines_list:
                            lines_list.append(new_line)
                            if self.player_turn == 1:
                                self.p1_score += 1
                                self.p1_score_label.config(text="Player 1 score: " + str(self.p1_score))
                            else:
                                self.p2_score += 1
                                self.p2_score_label.config(text="Player 2 score: " + str(self.p2_score))
            for line in diagonal_master1:
                for n in range(1, len(line)-1):
                    if line[n+1][1] == line[n][1] + 1 and line[n][1] == line[n-1][1] + 1:
                        new_line = [line[n-1], line[n], line[n+1]]
                        if new_line not in lines_list:
                            lines_list.append(new_line)
                            if self.player_turn == 1:
                                self.p1_score += 1
                                self.p1_score_label.config(text="Player 1 score: " + str(self.p1_score))
                            else:
                                self.p2_score += 1
                                self.p2_score_label.config(text="Player 2 score: " + str(self.p2_score))
            for line in diagonal_master2:
                for n in range(1, len(line)-1):
                    if line[n+1][0] == line[n][0] + 1 and line[n][0] == line[n-1][0] + 1:
                        new_line = [line[n-1], line[n], line[n+1]]
                        if new_line not in lines_list:
                            lines_list.append(new_line)
                            if self.player_turn == 1:
                                self.p1_score += 1
                                self.p1_score_label.config(text="Player 1 score: " + str(self.p1_score))
                            else:
                                self.p2_score += 1
                                self.p2_score_label.config(text="Player 2 score: " + str(self.p2_score))

    def message_destroy(self, message):
        message.destroy()

    def player_messenger(self):
        if self.player_turn == 1:
            self.p1_message = tkinter.Label(self.frame, text="Player 1\n Place your tile",
                                            font="gothic 20 bold", anchor="w", bg="#D4BFA8")
            self.p1_message.grid(row=1, column=0)
        else:
            self.p2_message = tkinter.Label(self.frame, text="Player 2\n Place your tile",
                                            font="gothic 20 bold", anchor="e", bg="#D4BFA8")
            self.p2_message.grid(row=1, column=3)

    def win_message(self):
        p1_label = tkinter.Label(self.frame, text="Player 1 score: "+str(self.p1_score), font="none 18 bold").grid(row=0, column=0, sticky="w")
        p2_label = tkinter.Label(self.frame, text="Player 2 score: "+str(self.p2_score), font="none 18 bold").grid(row=0, column=3, sticky="e")
        if self.p1_score > self.p2_score:
            win_label = tkinter.Label(self.board_frame, text="Congratulations\n Player 1!\n You Win!", font="gothic 18 bold").grid(row=1, column=1, columnspan=2)
        elif self.p2_score > self.p1_score:
            win_label = tkinter.Label(self.board_frame, text="Congratulations\n Player 2!\n You Win!", font="gothic 18 bold").grid(row=1, column=1, columnspan=2)
        else:
            win_label = tkinter.Label(self.board_frame, text="Good Game!\n It's a Draw", font="gothic 18 bold").grid(row=1, column=1, columnspan=2)

class Board(object):
    def __init__(self, game, shape):
        self.game = game
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
                b = BoardSquare(self.game, self, i, j)
                row_list.append(b)
                row_list[j-column_start].square.grid(row=i, column=j)
            self.board_list.append(row_list)

    def board_build1(self, rows, columns):
        for i in range(rows):
            row_list = []
            for j in range(columns):
                b = BoardSquare(self.game, self, i, j)
                row_list.append(b)
                row_list[j].square.grid(row=i, column=j)
            self.board_list.append(row_list)


class TileSet(object):
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.tile_list = []
        self.tile_set_builder()

    def tile_set_builder(self):
        for i in range(2):
            row = []
            for j in range(1, 5):
                t = Tile(self.game, self, self.player, i, j)
                row.append(t)
            self.tile_list.append(row)


class BoardSquare(object):
    def __init__(self, game, board, row, column):
        side = 15
        height = 7
        self.game = game
        self.board = board
        self.row = row
        self.column = column
        self.square = tkinter.Label(self.game.board_frame, height=height, width=side, relief="groove", bg="#B7DEB3")
        self.square.bind("<Button-1>", self.tile_placer)
        self.active = True
        self.tiled = False

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
                return
            elif self.game.player_turn == 1:
                if self.game.p1_tiles_remaining == 0:
                    for row in self.game.board.board_list:
                        for board_square in row:
                            board_square.active = False
                    self.game.message_destroy(self.game.p1_message)
                    self.game.message_destroy(self.game.p2_message)
                    self.game.win_message()
                    return
                self.tiled = True
                self.active = False
                self.game.turn += 1
                self.game.p1_tiles_placed.append([self.row, self.column])
                self.game.p1_tiles_placed.sort()
                if self.game.tile_select == 1:
                    self.straight_changer()
                    self.tile_image_move(straightp1_img)
                elif self.game.tile_select == 2:
                    self.diag_changer()
                    self.tile_image_move(diagonalp1_img)
                elif self.game.tile_select == 3:
                    self.pull_changer()
                    self.tile_image_move(pullerp1_img)
                elif self.game.tile_select == 4:
                    self.push_changer()
                    self.tile_image_move(pusherp1_img)

                self.game.line_checker(self.game.p1_tiles_placed, self.game.p1_lines_list)
                self.game.p1_tiles_remaining -= 1
                if self.game.p2_tiles_remaining == 0 or not self.turn_switch() and self.game.p1_tiles_remaining == 0:
                    self.end_game()
                else:
                    self.game.message_destroy(self.game.p1_message)
                    self.game.message_destroy(self.game.p2_message)
                    self.game.player_messenger()
                    self.game.tile_select = 0

            elif self.game.player_turn == -1:
                if self.game.p2_tiles_remaining == 0:
                    for row in self.game.board.board_list:
                        for board_square in row:
                            board_square.active = False
                    self.game.message_destroy(self.game.p1_message)
                    self.game.message_destroy(self.game.p2_message)
                    self.game.win_message()
                    return
                self.tiled = True
                self.active = False
                self.game.turn += 1
                self.game.p2_tiles_placed.append([self.row, self.column])
                self.game.p2_tiles_placed.sort()
                if self.game.tile_select == 1:
                    self.straight_changer()
                    self.tile_image_move(straightp2_img)
                elif self.game.tile_select == 2:
                    self.diag_changer()
                    self.tile_image_move(diagonalp2_img)
                elif self.game.tile_select == 3:
                    self.pull_changer()
                    self.tile_image_move(pullerp2_img)
                elif self.game.tile_select == 4:
                    self.push_changer()
                    self.tile_image_move(pusherp2_img)

                self.game.line_checker(self.game.p2_tiles_placed, self.game.p2_lines_list)
                self.game.p2_tiles_remaining -= 1
                if self.game.p1_tiles_remaining == 0 or not self.turn_switch() and self.game.p2_tiles_remaining == 0:
                    self.end_game()
                else:
                    self.game.message_destroy(self.game.p1_message)
                    self.game.message_destroy(self.game.p2_message)
                    self.game.player_messenger()
                    self.game.tile_select = 0
            self.game.tile_select = 0


    def reset_board(self):
        for row in self.board.board_list:
            for square in row:
                if not square.tiled:
                    square.square.config(bg="#B7DEB3")
                    square.active = True

    def straight_changer(self):
        self.reset_board()
        for row in self.board.board_list:
            for square in row:
                if not square.tiled:
                    if square.row == self.row or square.column == self.column:
                        square.square.config(bg="#B7DEB3")
                    else:
                        square.active = False
                        square.square.config(bg="#BF9696")
                else:
                    square.square.config(bg="#A6A599")

    def diag_changer(self):
        self.reset_board()
        for row in self.board.board_list:
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
        for row in self.board.board_list:
            for square in row:
                if not square.tiled:
                    if self.column - 1 <= square.column <= self.column+1 and self.row - 1 <= square.row <= self.row + 1:
                        square.square.config(bg="#BF9696")
                        square.active = False
                    else:
                        square.square.config(bg="#B7DEB3")

    def turn_switch(self):
        for row in self.board.board_list:
            for square in row:
                if square.active and not square.tiled:
                    self.game.player_turn *= -1
                    return True
        self.reset_board()
        return False

    def end_game(self):
        for row in self.game.board.board_list:
            for board_square in row:
                board_square.active = False
        self.game.message_destroy(self.game.p1_message)
        self.game.message_destroy(self.game.p2_message)
        self.game.win_message()

    def tile_image_move(self, image):
        self.square = tkinter.Label(self.game.board_frame, image=image, borderwidth=0)
        self.square.image = image
        self.square.grid(row=self.row, column=self.column)
        if self.game.player_turn == 1:
            self.game.p1_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label.destroy()
            self.game.p1_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label = \
                tkinter.Label(self.game.p1_tile_frame, height=7, width=15, relief="sunken", padx=2, pady=2, bg="#A6A599")
            self.game.p1_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label.\
                grid(row=self.game.tile_row, column=self.game.tile_select-1)
        elif self.game.player_turn == -1:
            self.game.p2_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label.destroy()
            self.game.p2_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label = \
                tkinter.Label(self.game.p2_tile_frame, height=7, width=15, relief="sunken", padx=2, pady=2, bg="#A6A599")
            self.game.p2_tile_set.tile_list[self.game.tile_row][self.game.tile_select-1].label.\
                grid(row=self.game.tile_row, column=self.game.tile_select-1)


class Tile(object):
    def __init__(self, game, t_set, p, row, typ):
        straightp1_img = tkinter.PhotoImage(file="straightp1.gif")
        diagonalp1_img = tkinter.PhotoImage(file="diagonalp1.gif")
        pullerp1_img = tkinter.PhotoImage(file="pullerp1.gif")
        pusherp1_img = tkinter.PhotoImage(file="pusherp1.gif")
        straightp2_img = tkinter.PhotoImage(file="straightp2.gif")
        diagonalp2_img = tkinter.PhotoImage(file="diagonalp2.gif")
        pullerp2_img = tkinter.PhotoImage(file="pullerp2.gif")
        pusherp2_img = tkinter.PhotoImage(file="pusherp2.gif")

        self.tile_set = t_set
        self.game = game
        self.label = None
        self.player_belongs = p
        self.type = typ
        self.row = row
        if self.player_belongs == 1:
            if self.type == 1:
                self.tile_definer(straightp1_img, self.game.p1_tile_frame)
            elif self.type == 2:
                self.tile_definer(diagonalp1_img, self.game.p1_tile_frame)
            elif self.type == 3:
                self.tile_definer(pullerp1_img, self.game.p1_tile_frame)
            elif self.type == 4:
                self.tile_definer(pusherp1_img, self.game.p1_tile_frame)
        if self.player_belongs == -1:
            if self.type == 1:
                self.tile_definer(straightp2_img, self.game.p2_tile_frame)
            elif self.type == 2:
                self.tile_definer(diagonalp2_img, self.game.p2_tile_frame)
            elif self.type == 3:
                self.tile_definer(pullerp2_img, self.game.p2_tile_frame)
            elif self.type == 4:
                self.tile_definer(pusherp2_img, self.game.p2_tile_frame)

    def tile_definer(self, image, frame):
        self.label = tkinter.Label(frame, image=image, height=95, width=94, relief="sunken")
        self.label.image = image
        self.label.bind("<Button-1>", self.tile_selector)
        self.label.grid(row=self.row, column=self.type-1)

    def tile_selector(self, event):
        if self.player_belongs == self.game.player_turn:
            for row in self.tile_set.tile_list:
                for tile in row:
                    tile.label.config(relief="sunken")
            self.label.config(relief="raised")
            self.game.tile_select = self.type
            self.game.tile_row = self.row


main_window = MainWindow()
main_window.root.mainloop()
