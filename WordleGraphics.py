# File: WordleGraphics.py

"""
This file implements the WordleGWindow class, which manages the
graphical display for the Wordle project.
"""

import atexit
import math
import time
import tkinter
# from Wordle import WordleClass
# from logic import WordleLogic
from WordleDictionary import FIVE_LETTER_WORDS
import random
import sys

# Constants

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

CORRECT_COLOR = "#66BB66"       # Light green for correct letters
PRESENT_COLOR = "#CCBB66"       # Brownish yellow for misplaced letters
MISSING_COLOR = "#999999"       # Gray for letters that don't appear
UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
KEY_COLOR = "#DDDDDD"           # Keys are colored light gray

#alternate colors
CORRECT_COLOR_ALTERNATE = "#113A6B"       # Blue for correct letters
PRESENT_COLOR_ALTERNATE = "#84AFE3"       # Light Pink for misplaced letters
MISSING_COLOR_ALTERNATE = "#E9DFF2"       # Light purple for letters that don't appear

CANVAS_WIDTH = 500		# Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 700		# Height of the tkinter canvas (pixels)

SQUARE_SIZE = 60		# Size of each square (pixels)
SQUARE_SEP = 5                  # Separation between squares (pixels)
TOP_MARGIN = 30    		# Top margin (pixels)
BOTTOM_MARGIN = 30    		# Bottom margin (pixels)
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = ("Helvetica Neue", -44, "bold")
MESSAGE_FONT = ("Helvetica Neue", -20, "bold")
KEY_FONT = ("Helvetica Neue", -18)
ENTER_FONT = ("Helvetica Neue", -14)

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

CLICK_MAX_DISTANCE = 2
CLICK_MAX_DELAY = 0.5

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = CANVAS_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

class WordleGWindow:
    """This class creates the Wordle window."""

    def __init__(self):
        """Creates the Wordle window."""
        # super(WordleGWindow, self).__init__()
        # self.setWindowTitle("Toggle Button")
        self.stats_list = [] # each time a correct answer is guessed, the row number of the guess will be appended to to stats_list
        self.round_number = 0 #this number advances each time the player guesses a correct word
        def create_grid():
            return [
                [
                    WordleSquare(canvas, i, j) for j in range(N_COLS)
                ] for i in range(N_ROWS)
            ]

        def create_keyboard():
            keys = { }
            nk = len(KEY_LABELS[0])
            h = KEY_HEIGHT
            y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
            for row in range(len(KEY_LABELS)):
                y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                if row == 1:
                    x += (KEY_WIDTH + KEY_XSEP) / 2
                for col in range(len(KEY_LABELS[row])):
                    label = KEY_LABELS[row][col]
                    w = KEY_WIDTH
                    if len(label) > 1:
                        w += (KEY_WIDTH + KEY_XSEP) / 2
                    keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                    x += w + KEY_XSEP
            #ADD TOGGLE KEY
            keys["toggle"] = WordleKey(self._canvas, 10, 75, 70, 30, "Color")
           
            #Add key to play game again and reset board
            keys["share"] = WordleKey(self._canvas, 10, 115, 70, 30, "Share")

             #Add key to show stats from past rounds 
            # keys["stats"] = WordleKey(self._canvas, 10, 155, 70, 30, "Stats")
            return keys
        
            
        def create_message():
            return WordleMessage(self._canvas,
                                 CANVAS_WIDTH / 2,
                                 MESSAGE_Y)

        def key_action(tke):
            if isinstance(tke, str):
                ch = tke.upper()
            else:
                ch = tke.char.upper()
            if ch == "\007" or ch == "\177" or ch == "DELETE":
                self.show_message("")
                if self._row < N_ROWS and self._col > 0:
                    self._col -= 1
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(" ")
            elif ch == "SHARE": #if the Replay button is pressed, clear board annd start over 
                for row in range(N_ROWS):
                    for col in range(N_COLS):
                        self.set_square_letter(row, col, " ")
                        # self.set_square_color(row, col, UNKNOWN_COLOR)
                # self.set_current_row(0)
                # self.wordle2()
                guessCount = str(self.get_current_row) 
                self.show_message("Congratulations! Share your results with friends!")
            elif ch == "STATS":
                self.show_message("These are your stats")
                #print stats_list with new line 
                # self.show_message(self.stats_list)
                

            elif ch == "COLOR": #If the color button is pressed, change the color scheme
                self.set_current_color_scheme()
                self.show_message("COLOR SCHEME CHANGED")
                curr_row = self.get_current_row()
                #The below code goes row by row and checks each letter for current color, and then changes it to match the current
                #color scheme.
                if (curr_row > 0):
                    change_row = 0
                    while change_row <= curr_row:
                        curr_letter = 0 
                        while curr_letter < 5:
                            if((self.get_square_color(change_row, curr_letter) == CORRECT_COLOR)):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("CORRECT"))
                            elif((self.get_square_color(change_row, curr_letter) == CORRECT_COLOR_ALTERNATE)):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("CORRECT"))
                            elif((self.get_square_color(change_row, curr_letter) == PRESENT_COLOR)):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("PRESENT"))
                            elif (self.get_square_color(change_row, curr_letter) == PRESENT_COLOR_ALTERNATE):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("PRESENT"))
                            elif((self.get_square_color(change_row, curr_letter) == MISSING_COLOR)):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("MISSING"))
                            elif(self.get_square_color(change_row, curr_letter) == MISSING_COLOR_ALTERNATE):
                                self.set_square_color(change_row, curr_letter, self.get_letter_color("MISSING"))
                            curr_letter = curr_letter + 1
                        change_row = change_row + 1
            
            elif ch == "\r" or ch == "\n" or ch == "ENTER":
                self.show_message("")
                s = ""
                for col in range(N_COLS):
                    s += self._grid[self._row][col].get_letter();
                for fn in self._enter_listeners:
                    fn(s)
            elif ch.isalpha():
                self.show_message("")
                if self._row < N_ROWS and self._col < N_COLS:
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(ch)
                    self._col += 1
           
        
      


        def press_action(tke):
            self._down_x = tke.x
            self._down_y = tke.y
            self._down_time = time.time()

        def release_action(tke):
            if abs(self._down_x - tke.x) <= CLICK_MAX_DISTANCE:
                if abs(self._down_y - tke.y) <= CLICK_MAX_DISTANCE:
                    t = time.time()
                    if t - self._down_time < CLICK_MAX_DELAY:
                        key = find_key(tke.x, tke.y)
                        if key:
                            key_action(key._label)

        def find_key(x, y):
            for key in self._keys.values():
                kx, ky, kw, kh = key._bounds
                if x >= kx and x <= kx + kw and y >= ky and y <= ky + kh:
                    return key
            return None

        def delete_window():
            """Closes the window and exits from the event loop."""
            root.destroy()

        def start_event_loop():
            """Starts the tkinter event loop when the program exits."""
            root.mainloop()

        root = tkinter.Tk()
        root.title("Wordle")
        root.protocol("WM_DELETE_WINDOW", delete_window)
        self._root = root
        canvas = tkinter.Canvas(root,
                                bg="White",
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                highlightthickness=0)
        canvas.pack()
        self._canvas = canvas
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._enter_listeners = [ ]
        root.bind("<Key>", key_action)
        root.bind("<ButtonPress-1>", press_action)
        root.bind("<ButtonRelease-1>", release_action)
        self._row = 0
        self._col = 0
        self.color_scheme = "Default"
        atexit.register(start_event_loop)

    def get_square_letter(self, row, col):
        return self._grid[row][col].get_letter()

    def set_square_letter(self, row, col, ch):
        self._grid[row][col].set_letter(ch)

    def get_square_color(self, row, col):
        return self._grid[row][col].get_color()

    def set_square_color(self, row, col, color):
        self._grid[row][col].set_color(color)

    def get_key_color(self, ch):
        return self._keys[ch].get_color()

    def set_key_color(self, ch, color):
        self._keys[ch].set_color(color)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_letter(row, col, " ")
            self.set_square_color(row, col, UNKNOWN_COLOR)

    def add_enter_listener(self, fn):
        self._enter_listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)

    def set_current_color_scheme(self):
        if (self.color_scheme == "Default"):
            self.color_scheme = "Alternate"
        elif (self.color_scheme == "Alternate"):
            self.color_scheme = "Default"

    def get_letter_color(self, type):
        if (type == "CORRECT"):
            if (self.color_scheme == "Default"):
                return CORRECT_COLOR
            else:
                return CORRECT_COLOR_ALTERNATE
        elif (type == "PRESENT"):
            if (self.color_scheme == "Default"):
                return PRESENT_COLOR
            else:
                return PRESENT_COLOR_ALTERNATE
        elif (type == "MISSING"):
            if (self.color_scheme == "Default"):
                return MISSING_COLOR
            else:
                return MISSING_COLOR_ALTERNATE


    # def wordle2(self):

    #     #pick random word for the answer from word list
    #     word_list= []
    #     word_file = FIVE_LETTER_WORDS
    #     for word in word_file:
    #         word_list.append(word.strip())
        
    #     #pick a word
    #     answer = random.choice(word_list)
    #     answer = answer.upper()
    #     print(answer) #prints the answer in the terminal to help with testing
        
    #     #once the user hits enter, run the function below
    #     def enter_action(s):  #s is the user's guess
    #         r = s.lower() # r is the lower case version of the user's 
    #         position = 0 #setting initial column position 
    #         print(r) #prints lower case version of user guess in terminal 
            
    #         if s == answer: #check if user guessed correct answer
    #             self.show_message("Congratulations, You Won!") 
    #             # self.round_number += 1 #advance round number 
    #             # self.stats_list.append(str(self.round_number) + " " + str(self.get_current_row()) + " guesses n/") #append number of guesses for this round to stats_list
    #             print(self.stats_list)
    #             for letter in s:
    #                 if letter == answer[position]:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("CORRECT")) #color green
    #                 #letter in answer but not in the same position
    #                 elif letter in answer:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("PRESENT")) #color yellow
    #                 else:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("MISSING")) #color grey
    #                     self.get_current_row()
    #                 #move to next column/letter
    #                 position += 1
    #         elif r in word_list and r != answer: #check if user guessed a word from the list 
    #             self.show_message("Not the correct word")
                
    #             for letter in s:
    #                 if letter == answer[position]:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("CORRECT")) #color green
    #                 #letter in answer but not in the same position
    #                 elif letter in answer:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("PRESENT")) #color yellow
    #                 else:
    #                     self.set_square_color(self.get_current_row(), position, self.get_letter_color("MISSING")) #color grey

    #                 #move to next column/letter
    #                 position += 1
                
    #                 #if previous word is not correct, call this fucntion to move rows
    #             if (self.get_current_row() >= 5):
    #                 #ran out of turns
    #                 self.show_message("YOU LOSE!")
    #             else:
    #                 self.set_current_row((self.get_current_row() + 1))
    #         else:
    #             self.show_message("Not in word list")
            
            



    #     # gw = WordleGWindow()
    #     self.add_enter_listener(enter_action)



















class WordleSquare:

    def __init__(self, canvas, row, col):
        x0 = (CANVAS_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y0 = TOP_MARGIN + row * SQUARE_DELTA
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE
        self._canvas = canvas
        self._ch = " "
        self._color = UNKNOWN_COLOR;
        self._frame = canvas.create_rectangle(x0, y0, x1, y1)
        self._text = canvas.create_text(x0 + SQUARE_SIZE / 2,
                                        y0 + SQUARE_SIZE / 2,
                                        text=self._ch,
                                        font=SQUARE_FONT)

    def get_letter(self):
        return self._ch

    def set_letter(self, ch):
        self._ch = ch
        self._canvas.itemconfigure(self._text, text=ch)

    def get_color(self):
        return self._color

    def set_color(self, color):
        color = color.upper()
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleKey:

    def __init__(self, canvas, x, y, width, height, label):
        self._canvas = canvas
        self._label = label
        self._bounds = [ x, y, width, height ]
        self._color = UNKNOWN_COLOR
        font = KEY_FONT
        if label == "ENTER":
            font = ENTER_FONT
        if label == "DELETE":
            label = "\u232B"
        points = [ x + KEY_CORNER, y,
                   x + KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width, y,
                   x + width, y + KEY_CORNER,
                   x + width, y + KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x, y + height,
                   x, y + height - KEY_CORNER,
                   x, y + height - KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y]
        self._frame = canvas.create_polygon(points,
                                            fill=KEY_COLOR,
                                            outline=KEY_COLOR,
                                            smooth=True)
        self._text = canvas.create_text(x + width / 2,
                                        y + height / 2,
                                        text=label,
                                        font=font)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleMessage:

    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._text = ""
        self._msg = canvas.create_text(x, y,
                                       text="",
                                       font=MESSAGE_FONT,
                                       anchor=tkinter.CENTER)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._canvas.itemconfigure(self._msg, text=text, fill=color)
