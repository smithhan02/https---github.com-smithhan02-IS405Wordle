# File: Wordle.py

"""
This file contains the logic and implementation of the Wordle assignment. 
Section 1 Team 15
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys


class WordleClass:
    # def __init__(self):

    stats_list = [] # each time a correct answer is guessed, the row number of the guess will be appended to to stats_list
    round_number = 0 #this number advances each time the player guesses a correct word

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
            r = s.lower() # r is the lower case version of the user's 
            position = 0 #setting initial column position 
            print(r) #prints lower case version of user guess in terminal 
            
            if s == answer: #check if user guessed correct answer
                gw.show_message("Congratulations, You Won!") 
                self.round_number += 1 #advance round number 
                self.stats_list.append(str(self.round_number) + " " + gw.get_current_row() + " guesses n/") #append number of guesses for this round to stats_list

                for letter in s:
                    if letter == answer[position]:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("CORRECT")) #color green
                    #letter in answer but not in the same position
                    elif letter in answer:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("PRESENT")) #color yellow
                    else:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("MISSING")) #color grey
                        gw.get_current_row()
                    #move to next column/letter
                    position += 1
            elif r in word_list and r != answer: #check if user guessed a word from the list 
                gw.show_message("Not the correct word")
                
                for letter in s:
                    if letter == answer[position]:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("CORRECT")) #color green
                    #letter in answer but not in the same position
                    elif letter in answer:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("PRESENT")) #color yellow
                    else:
                        gw.set_square_color(gw.get_current_row(), position, gw.get_letter_color("MISSING")) #color grey

                    #move to next column/letter
                    position += 1
                
                    #if previous word is not correct, call this fucntion to move rows
                if (gw.get_current_row() >= 5):
                    #ran out of turns
                    gw.show_message("YOU LOSE!")
                else:
                    gw.set_current_row((gw.get_current_row() + 1))
            else:
                gw.show_message("Not in word list")
            
            



        gw = WordleGWindow()
        gw.add_enter_listener(enter_action)


    # Startup code
    if __name__ == "__main__":
        wordle()
    #test

    