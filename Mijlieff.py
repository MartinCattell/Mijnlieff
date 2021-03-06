import tkinter

class MainWindow(object):

    def __init__(self):
        self.root = tkinter.Tk()  # Tk main window
        self.root.wm_iconbitmap("straightp2_2.ico")
        self.root.config(bg="#D4BFA8")
        self.root.title("Mijnlieff")
        self.root.resizable(0, 0)  # Fix size
        tkinter.Label(self.root, text="Mijnlieff", font=("gothic", 24, "bold underline"), bg="#D4BFA8").grid(row=0, column=0, padx=40, pady=10)
        tkinter.Label(self.root, text="Select a board shape",font="msserif 8", bg="#D4BFA8").grid(row=1, column=0)

        self.board_shape = 0
        self.board_shape_images = [
            tkinter.PhotoImage(file="Square.gif"),
            tkinter.PhotoImage(file="Line.gif"),
            tkinter.PhotoImage(file="L.gif"),
            tkinter.PhotoImage(file="T.gif"),
            tkinter.PhotoImage(file="S.gif")
        ]

        self.shape_image = self.board_shape_images[self.board_shape]
        self.shape_button = tkinter.Button(self.root, image=self.shape_image, command=self.shape_changer, borderwidth=0, highlightthickness=0)
        self.shape_button.grid(row=2, column=0)

        tkinter.Button(self.root, text="Start Game", font="msserif 14", command=self.start_game, bg="#A18B73").grid(row=4, column=0, pady=15)

    def shape_changer(self):
        self.board_shape += 1
        if 4 < self.board_shape:
            self.board_shape = 0
        self.shape_image = self.board_shape_images[self.board_shape]
        self.shape_button = tkinter.Button(self.root, image=self.shape_image, command=self.shape_changer,  borderwidth=0, highlightthickness=0)
        self.shape_button.grid(row=2, column=0)    
        
    def start_game(self):
        game_window = tkinter.Toplevel(bg="#D4BFA8")
        game_window.wm_iconbitmap("straightp2_2.ico")
        game_window.title("Mijnlieff")
        game_window.resizable(0, 0)
        game_window.grab_set()

        Game(game_window, self.board_shape)


class Game(object):
    def __init__(self, frame, board_shape):
        self.frame = frame
        self.frame.bind("<Enter>", self.do_nothing)
        self.tile_images = [
            [
            tkinter.PhotoImage(file="straightp1.gif"),
            tkinter.PhotoImage(file="diagonalp1.gif"),
            tkinter.PhotoImage(file="pullerp1.gif"),
            tkinter.PhotoImage(file="pusherp1.gif")],
            [
            tkinter.PhotoImage(file="straightp2.gif"),
            tkinter.PhotoImage(file="diagonalp2.gif"),
            tkinter.PhotoImage(file="pullerp2.gif"),
            tkinter.PhotoImage(file="pusherp2.gif")]
        ]

        self.player_1 = Player(self, 1)
        self.player_2 = Player(self, 2)
        self.player_list = [self.player_1, self.player_2]

        self.player_1.score_label.grid(row=0, column=0, sticky="w",  padx=50, pady=10)
        self.player_2.score_label.grid(row=0, column=4, sticky="e",  padx=50, pady=10)
        self.player_1.tile_set.tile_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.player_2.tile_set.tile_frame.grid(row=2, column=3, columnspan=2, sticky="e", padx=10, pady=10)

        self.board_frame = tkinter.Frame(self.frame, bg="#D4BFA8")
        self.board_frame.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
        self.board = Board(self, board_shape)

        self.player_turn = 1    
        self.selected_tile = 0
        self.cdimage = None
        self.tile_row = 0
        self.player = 0
        self.was_clicked = False

        self.player_1.message.grid(row=1, column=4*(self.player_1.number-1))


    def turn_switch_check(self):
        for row in self.board.board_list:
            for board_square in row:
                if board_square.active and not board_square.tiled:
                    self.player_turn = -(self.player_turn-3)
                    return True
        self.board.reset_board()
        return False


# Detects new lines when a player places a tile. It takes the most recent tile (position) A (before it is added to the player's list)
# and checks for contiguous tiles. If none are found A is added to the player's list and the game proceeds. 
# If contiguous tiles B are found their relationship to A is determined and hypothetical tiles C and Z are created. 
# C is to B as B is to A and Z is to A as A is to B. 
# If C or Z exists in player's list [A, B, C] or [B, A, Z] are valid lines and the player's score is increased by one.  
# If BAZ is added then the player's score is reduced by 0.5 because this line will be found twice.
    def line_finder(self, player, row, column):
        A = [row, column]
        B_check_list = []
        C = [None, None]
        Z = [None, None]
        for place in player.tiles_placed:
            if A[0]-2 < place[0] < A[0]+2 and  A[1]-2 < place[1] < A[1]+2:
                B_check_list.append(place)
        if B_check_list:
            for B in B_check_list:
                if A[0] == B[0]:
                    C = [A[0], B[1] + (B[1]-A[1])]
                    Z = [B[0], A[1] + (A[1]-B[1])]
                elif A[1] == B[1]:
                    C = [B[0] + (B[0]-A[0]), A[1]]
                    Z = [A[0] + (A[0]-B[0]), B[1]]
                else:
                    if A[0] == B[0]-1:
                        C[0] = B[0]+1
                        Z[0] = A[0]-1
                    else: 
                        C[0] = B[0]-1
                        Z[0] = A[0]+1

                    if A[1] == B[1]-1:
                        C[1] = B[1]+1
                        Z[1] = A[1]-1
                    else: 
                        C[1] = B[1]-1
                        Z[1] = A[1]+1

                if C in player.tiles_placed:
                    player.score += 1
                if Z in player.tiles_placed:
                    player.score += 0.5
            player.score_label.config(text=player.string + " score: " + str(int(player.score)))
        player.tiles_placed.append(A)
        player.tiles_remaining -= 1
        self.selected_tile = 0

    def win_message(self):
        self.player_1.score_label.config(text="Player 1 score: "+str(self.player_1.score))
        self.player_2.score_label.config(text="Player 2 score: "+str(self.player_2.score))
        if self.player_1.score > self.player_2.score:
            tkinter.Label(self.frame, text="Congratulations\n Player 1!\n You Win!", font="gothic 18 bold", bg="#D4BFA8").grid(row=2, column=1, columnspan=3)
        elif self.player_2.score > self.player_1.score:
            tkinter.Label(self.frame, text="Congratulations\n Player 2!\n You Win!", font="gothic 18 bold", bg="#D4BFA8").grid(row=2, column=1, columnspan=3)
        else:
            tkinter.Label(self.frame, text="Good Game!\n It's a Draw  ", font="gothic 18 bold", bg="#D4BFA8").grid(row=2, column=1, columnspan=3)

    def end_game(self):
        for row in self.board.board_list:
            for board_square in row:
                board_square.active = False
                board_square.square_label.config(bg=board_square.cant_place)
        self.player_1.message.grid_forget()
        self.player_2.message.grid_forget()
        self.win_message()

    def turn_decider(self, current_player):
        next_player = self.player_list[-(current_player.number-2)]
        if next_player.tiles_remaining == 0 or not self.turn_switch_check() and current_player.tiles_remaining == 0:
            self.end_game()
        else:
            current_player.message.grid_forget()
            current_player.message2.grid_forget()
            
            if current_player.number != self.player_turn:
                next_player.message.grid(row=1, column=4*(next_player.number-1))
            else:
                current_player.message2.grid(row=1, column=4*(current_player.number-1))

    def cdimage_updater(self):
        self.selected_tile = 0
        self.cdimage.unbind("<Motion>")
        self.frame.unbind("<Motion>")
        self.cdimage.destroy()
        self.was_clicked = False

    def do_nothing(self, event):
        if self.selected_tile > 0:
            self.cdimage.geometry("95x95+" + str(self.frame.winfo_pointerx()-50) + "+" + str(self.frame.winfo_pointery()-50))
            
class Player(object):
    def __init__(self, game, number):
        self.game = game
        self.number = number
        
        self.string = "Player " + str(self.number)
        self.tiles_placed = []
        self.tiles_remaining = 8
        self.score = 0
        self.straight_img = self.game.tile_images[self.number-1][0]
        self.diagonal_img = self.game.tile_images[self.number-1][1]
        self.puller_img = self.game.tile_images[self.number-1][2]
        self.pusher_img = self.game.tile_images[self.number-1][3]

        self.score_label = tkinter.Label(self.game.frame, text=self.string + " score: 0", font="none 18 bold")
        self.message = tkinter.Label(self.game.frame, text=self.string + "\n Place your tile", font="gothic 24 bold", anchor="w", bg="#D4BFA8")
        self.message2 = tkinter.Label(self.game.frame, text=self.string + "\n again!", font="gothic 24 bold", anchor="w", bg="#D4BFA8")
        
        self.tile_set = TileSet(self.game, self)


class Board(object):
    def __init__(self, game, shape):
        self.game = game
        self.board_list = []
        if shape == 0:
            self.board_build1(4, 4)
        elif shape == 1:
            self.board_build1(2, 8)
        elif shape == 2:
            self.board_build2(4, 0, 2, 1, 0, 6)
        elif shape == 3:
            self.board_build2(4, 2, 4, 1, 0, 6)
        elif shape == 4:
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
                row_list[j-column_start].square_label.grid(row=i, column=j)
            self.board_list.append(row_list)

    def board_build1(self, rows, columns):
        for i in range(rows):
            row_list = []
            for j in range(columns):
                b = BoardSquare(self.game, self, i, j)
                row_list.append(b)
                row_list[j].square_label.grid(row=i, column=j)
            self.board_list.append(row_list)

    def reset_board(self):
        for row in self.board_list:
            for board_square in row:
                if not board_square.tiled:
                    board_square.square_label.config(bg=board_square.can_place)
                    board_square.active = True

    def straight_changer(self, row, column):
        self.reset_board()
        for r in self.board_list:
            for board_square in r:
                if not board_square.tiled:
                    if board_square.row == row or board_square.column == column:
                        board_square.square_label.config(bg=board_square.can_place)
                    else:
                        board_square.active = False
                        board_square.square_label.config(bg=board_square.cant_place)
                else:
                    board_square.square_label.config(bg=board_square.cant_place)

    def diag_changer(self, row, column):
        self.reset_board()
        for r in self.board_list:
            c_1 = column - row
            c_2 = column + row
            for board_square in r:
                if not board_square.tiled:
                    if board_square.column == board_square.row + c_1 or board_square.column == -board_square.row + c_2:
                        board_square.square_label.config(bg=board_square.can_place)
                    else:
                        board_square.active = False
                        board_square.square_label.config(bg=board_square.cant_place)
                else:
                    board_square.square_label.config(bg=board_square.cant_place)

    def pull_changer(self, row, column):
        self.reset_board()
        for r in self.board_list:
            for board_square in r:
                if not board_square.tiled:
                    if column - 1 <= board_square.column <= column + 1 and row - 1 <= board_square.row <= row + 1:
                        board_square.square_label.config(bg=board_square.can_place)
                    else:
                        board_square.active = False
                        board_square.square_label.config(bg=board_square.cant_place)
                else:
                    board_square.square_label.config(bg=board_square.cant_place)

    def push_changer(self, row, column):
        self.reset_board()
        for r in self.board_list:
            for board_square in r:
                if not board_square.tiled:
                    if column - 1 <= board_square.column <= column + 1 and row - 1 <= board_square.row <= row + 1:
                        board_square.square_label.config(bg=board_square.cant_place)
                        board_square.active = False
                    else:
                        board_square.square_label.config(bg=board_square.can_place)
                else:
                    board_square.square_label.config(bg=board_square.cant_place)


class TileSet(object):
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.tile_frame = tkinter.Frame(self.game.frame, bg="#361800")
        self.tile_list = []
        self.tile_set_builder()
       

    def tile_set_builder(self):
        for i in range(2):
            row = []
            for j in range(1, 5):
                t = Tile(self.game, self, i, j)
                row.append(t)
                t.label.image = t.image
                t.label.grid(row=i, column=j-1, padx=5, pady=5)
            self.tile_list.append(row)
            
    def tile_remover(self):
        self.tile_list[self.game.tile_row][self.game.selected_tile-1].label.destroy()
        self.tile_list[self.game.tile_row][self.game.selected_tile-1].label = \
            tkinter.Label(self.tile_frame, height=6, width=13, relief="sunken", padx=2, pady=2, bg="#241000", bd=0)
        self.tile_list[self.game.tile_row][self.game.selected_tile-1].label.grid(row=self.game.tile_row, column=self.game.selected_tile-1, padx=5, pady=5)


class BoardSquare(object):
    def __init__(self, game, board, row, column):
        width = 15
        height = 7
        self.can_place = "#D7D7D7"
        self.cant_place = "#241000"
        self.game = game
        self.board = board
        self.row = row
        self.column = column

        self.square_label = tkinter.Label(self.game.board_frame, height=height, width=width, relief="groove", bg=self.can_place)
        self.square_label.bind("<Enter>", self.tile_placer)
        self.active = True
        self.tiled = False

    def tile_placer(self, event):
        if not self.active or self.game.selected_tile == 0 or not self.game.was_clicked:
            return

        for player in self.game.player_list:
            if player.number == self.game.player_turn:
                self.tiled = True
                self.active = False
                self.tile_image_chooser(player)
                player.tile_set.tile_remover()
                self.game.line_finder(player, self.row, self.column)
                self.game.turn_decider(player)
                break
        self.game.cdimage_updater()

    def tile_image_chooser(self, player):
        if self.game.selected_tile == 1:
            self.board.straight_changer(row=self.row, column=self.column)
            self.tile_image_placer(player.straight_img)
        elif self.game.selected_tile == 2:
            self.board.diag_changer(row=self.row, column=self.column)
            self.tile_image_placer(player.diagonal_img)
        elif self.game.selected_tile == 3:
            self.board.pull_changer(row=self.row, column=self.column)
            self.tile_image_placer(player.puller_img)
        elif self.game.selected_tile == 4:
            self.board.push_changer(row=self.row, column=self.column)
            self.tile_image_placer(player.pusher_img)

    def tile_image_placer(self, image):
        self.square_label = tkinter.Label(self.game.board_frame, image=image, borderwidth=0)
        self.square_label.image = image
        self.square_label.grid(row=self.row, column=self.column)


class Tile(object):
    def __init__(self, game, tile_set, row, typ):
        self.game = game
        self.tile_set = tile_set
        self.player = self.tile_set.player.number
        self.row = row
        self.type = typ
        self.label = None
        self.x = None
        self.y = None
        self.image = self.game.tile_images[self.player-1][self.type-1]
        self.frame = self.tile_set.tile_frame
        self.label = tkinter.Label(self.frame, image=self.image, height=95, width=94, highlightthickness=0, bd=0)
        
        self.label.bind("<Enter>", self.selected_tile_check)
        self.label.bind("<Button-1>", self.tile_selector)
        
    def tile_selector(self, event):
        if self.player == self.game.player_turn:
            self.game.selected_tile = self.type
            self.game.tile_row = self.row

            if(self.game.cdimage):
                self.game.cdimage.destroy()

            self.game.cdimage = tkinter.Toplevel(self.game.frame, bd=0, highlightthickness=0)
            self.game.cdimage.overrideredirect(1)
            self.x = self.game.frame.winfo_pointerx()
            self.y = self.game.frame.winfo_pointery()
            self.game.cdimage.geometry("95x95+" + str(self.x-50) + "+" + str(self.y-50))
            self.game.cdimage.attributes("-alpha", 0.5)

            cdlabel = tkinter.Label(self.game.cdimage, image=self.label.image, bd=0, highlightthickness=0)
            cdlabel.pack()

            self.game.frame.bind("<Motion>", self.outer_motion)
            self.game.cdimage.bind("<Motion>", self.inner_motion)
            self.game.cdimage.bind("<Button-1>", self.click_vanish)

    def cdimage_mover(self):
        if(self.x - 50 < self.game.frame.winfo_x()):
            self.x = self.game.frame.winfo_x()+60
        if(self.x + 50 > self.game.frame.winfo_x()+self.game.frame.winfo_width()):
            self.x = self.game.frame.winfo_x()+self.game.frame.winfo_width()-44
        if(self.y - 50 < self.game.frame.winfo_y()+25):
            self.y = self.game.frame.winfo_y()+80
        if(self.y + 50 > self.game.frame.winfo_y()+self.game.frame.winfo_height()):
            self.y = self.game.frame.winfo_y()+self.game.frame.winfo_height()-25
        self.game.cdimage.geometry("95x95+" + str(self.x-50) + "+" + str(self.y-50))

    def outer_motion(self, event):
        self.x = self.game.frame.winfo_pointerx()
        self.y = self.game.frame.winfo_pointery()
        self.cdimage_mover()
        
    def inner_motion(self, event):
        x = event.x
        y = event.y
        self.x += (x-50)
        self.y += (y-50)
        self.cdimage_mover()

    def click_vanish(self, event):
        self.game.cdimage.geometry("0x0+0+0")
        self.game.was_clicked = True

    def selected_tile_check(self, event):
        if (self.game.selected_tile > 0):
            self.label.event_generate("<Button-1>")


main_window = MainWindow()
main_window.root.mainloop()
