# File: Wordle.py

"""
This file contains the logic and implementation of the Wordle assignment. 
Section 1 Team 15
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS


CORRECT_COLOR = "#66BB66"       # Light green for correct letters
PRESENT_COLOR = "#CCBB66"       # Brownish yellow for misplaced letters
MISSING_COLOR = "#999999"       # Gray for letters that don't appear

def wordle():

    #pick random word for the answer from word list
    word_list= []
    word_file = FIVE_LETTER_WORDS
    for word in word_file:
        word_list.append(word.strip())

    #pick a word
    answer = random.choice(word_list)
    answer = answer.upper()
    print(answer) #prints the answer in the terminal to help with testing


    #once the user hits enter, run the function below
    def enter_action(s):  #s is the user's guess

        position = 0 #setting initial column position 
        for letter in s:
            if letter == answer[position]:
                gw.set_square_color(gw.get_current_row(), position, CORRECT_COLOR) #color green
            #letter in answer but not in the same position
            elif letter in answer:
                gw.set_square_color(gw.get_current_row(), position, PRESENT_COLOR) #color yellow
            else:
                gw.set_square_color(gw.get_current_row(), position, MISSING_COLOR) #color grey

            #move to next column/letter
            position += 1
        
        #if previous word is not correct, call this fucntion to move rows
        if (gw.get_current_row() >= 5):
            #ran out of turns
            gw.show_message("YOU LOSE!")
        else:
            gw.set_current_row((gw.get_current_row() + 1))


    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)


# Startup code
if __name__ == "__main__":
    wordle()
