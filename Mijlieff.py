import tkinter
import keyboard
import time


class MainWindow(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Mijnlieff")
        self.options_frame = tkinter.Frame(self.root)
        self.options_frame.grid(row=0, column=0, columnspan=2, sticky="w")
        self.new_game_button = tkinter.Button(self.options_frame, text="New Game", command=self.board_builder)
        self.new_game_button.grid(row=0, column=0)
        self.restart_game_button = tkinter.Button(self.options_frame, text="Restart")
        self.restart_game_button.grid(row=0, column=1)
        self.options_button = tkinter.Button(self.options_frame, text="Options", command=self.game_option_window)
        self.options_button.grid(row=0, column=2)
        self.quit_game_button = tkinter.Button(self.options_frame, text="Quit")
        self.quit_game_button.grid(row=0, column=3)
        self.game_frame = tkinter.Frame(self.root, height=50)
        self.game_frame.grid(row=1, column=0, columnspan=2)
        self.p1_tile_frame = tkinter.Frame(self.root, height=50, bg="green")
        self.p1_tile_frame.grid(row=2, column=0)
        self.p2_tile_frame = tkinter.Frame(self.root, height=50, bg="red")
        self.p2_tile_frame.grid(row=2, column=1)
        self.board_shape = 1


        self.board_list =[]
        for i in range(4):
            b = BoardSection(self.game_frame)
            self.board_list.append(b)

    def board_builder(self):
        if self.board_shape == 1:
            self.board_list[0].square_frame.grid(row=0, column=0)
            self.board_list[1].square_frame.grid(row=0, column=1)
            self.board_list[2].square_frame.grid(row=1, column=0)
            self.board_list[3].square_frame.grid(row=1, column=1)

        elif self.board_shape == 2:
            self.board_list[0].square_frame.grid(row=0, column=0)
            self.board_list[1].square_frame.grid(row=0, column=1)
            self.board_list[2].square_frame.grid(row=0, column=2)
            self.board_list[3].square_frame.grid(row=0, column=3)

        elif self.board_shape == 3:
            self.board_list[0].square_frame.grid(row=0, column=0)
            self.board_list[1].square_frame.grid(row=1, column=0)
            self.board_list[2].square_frame.grid(row=1, column=1)
            self.board_list[3].square_frame.grid(row=1, column=2)

        elif self.board_shape == 4:
            self.board_list[0].square_frame.grid(row=0, column=1)
            self.board_list[1].square_frame.grid(row=1, column=0)
            self.board_list[2].square_frame.grid(row=1, column=1)
            self.board_list[3].square_frame.grid(row=1, column=2)

        elif self.board_shape == 5:
            self.board_list[0].square_frame.grid(row=0, column=0)
            self.board_list[1].square_frame.grid(row=1, column=1)
            self.board_list[2].square_frame.grid(row=1, column=0)
            self.board_list[3].square_frame.grid(row=2, column=1)

    def board_shape1(self):
        self.board_shape = 1

    def board_shape2(self):
        self.board_shape = 2

    def board_shape3(self):
        self.board_shape = 3

    def board_shape4(self):
        self.board_shape = 4

    def board_shape5(self):
        self.board_shape = 5

    def game_option_window(self):
        global square_img
        global line_img
        global L_img
        global T_img
        global S_img
        options_window = tkinter.Toplevel()
        select_label = tkinter.Label(options_window, text="Select a board shape").grid(row=0, column=0)
        button_frame = tkinter.Frame(options_window, bg="green", height=50)
        square_img = tkinter.PhotoImage(file="Square.gif")
        square_button = tkinter.Button(button_frame, image=square_img, command=self.board_shape1)
        line_img = tkinter.PhotoImage(file="Line.gif")
        line_button = tkinter.Button(button_frame, image=line_img, command=self.board_shape2)
        L_img = tkinter.PhotoImage(file="L.gif")
        L_button = tkinter.Button(button_frame, image=L_img, command=self.board_shape3)
        T_img = tkinter.PhotoImage(file="T.gif")
        T_button = tkinter.Button(button_frame, image=T_img, command=self.board_shape4)
        S_img = tkinter.PhotoImage(file="S.gif")
        S_button = tkinter.Button(button_frame, image=S_img, command=self.board_shape5)

        square_button.grid(row=0, column=0)
        line_button.grid(row=0, column=2)
        L_button.grid(row=1, column=1)
        T_button.grid(row=2, column=0)
        S_button.grid(row=2, column=2)

        button_frame.grid(row=0, column=1)


class Game(object):
    def __init__(self):
        pass
    pass


class BoardSection(object):

    def __init__(self, frame):
        side = 110
        self.square_frame = tkinter.Frame(frame)
        self.subframe1 = tkinter.Frame(self.square_frame, height=side, width=side, bg="white")
        self.subframe2 = tkinter.Frame(self.square_frame, height=side, width=side, bg="black")
        self.subframe3 = tkinter.Frame(self.square_frame, height=side, width=side, bg="black")
        self.subframe4 = tkinter.Frame(self.square_frame, height=side, width=side, bg="white")
        self.subframe1.grid(row=0, column=0)
        self.subframe2.grid(row=0, column=1)
        self.subframe3.grid(row=1, column=0)
        self.subframe4.grid(row=1, column=1)


class Tile(object):
    def __init__(self, type):
        self.type = type
    pass


main_window = MainWindow()
main_window.root.mainloop()
