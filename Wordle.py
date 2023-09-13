# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS

def wordle():

    def processGuess(theAnswer, theGuess):
        position = 0
        clue = ""
        #check each letter in the guess
        for letter in theGuess:
            if letter == theAnswer[position]:
                clue += "G" #color green
            #letter in answer but not in the same position
            elif letter in theAnswer:
                clue += "Y"
            else:
                clue += "-"

            #check next letter
            position += 1
        print(clue)
        return clue == "GGGGG" #True if correct


    word_list= []
    word_file = FIVE_LETTER_WORDS
    for word in word_file:
        word_list.append(word.strip())

    #pick a word
    answer = random.choice(word_list)
    print(answer)

    num_of_guesses = 0
    guessed_correctly = False

    while num_of_guesses < 6 and not guessed_correctly:
        #get guess from user
        guess = input("Input a 5-letter word:  ")
        print("You have guessed the word: ", guess)
        num_of_guesses += 1

        #process guess
        guessed_correctly = processGuess(answer, guess)

    #display end of game message
    if guessed_correctly:
        print("Congrats! You won!")
    else:
        print("You lost.")





    #once the user hits enter, run the function below
    def enter_action(s):
        gw.show_message("You have to implement this method.")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code


if __name__ == "__main__":
    wordle()
