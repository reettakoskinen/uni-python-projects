"""
Reetta Koskinen

Balloon pop game. The game has tha same rules as hangman. You try to guess a
word by guessing what letters it has. There are six balloon that pop if you
make a mistake. If you guess the word before popping all the balloons you win.
If you pop all of the balloons before guessing the word you lose.
"""

from random import choice
from tkinter import *
from string import *


class Userinterface:
    """
    A class that represents a balloon pop game in a graphical user interface.
    """

    def __init__(self):
        """
        Constructor. Initiates a window and it's elements.
        """
        self.__main_window = Tk()
        self.__main_window.title("Balloon pop")

        # Game options widgets
        self.__leftframe = Frame(master=self.__main_window)
        self.__leftframe.grid(row=0, column=0, padx=30)

        # Gameplay widgets
        self.__rightframe = Frame(master=self.__main_window,
                                  background="white")
        self.__rightframe.grid(row=0, column=1)

        # Number of wrong answers allowed
        self.__balloons_left = None
        # Increased by one if a balloon is popped to move on to the next one
        self.__balloon_index = None
        # Show the player what letters have been guessed already
        self.__letters_not_in_word = None
        # The word that the player is trying to guess
        self.__word_to_be_guessed = None
        # For keeping score, increases by one for every game won
        self.__score = 0
        # For keeping score, increases by one for every game played
        self.__number_of_played_games = 0

        # Give instruction to choose a difficulty level
        self.__difficulty_label = Label(self.__leftframe,
                                        text=f"Start a new game\n by choosing "
                                             f"the\ndifficulty level\nand "
                                             f"pressing start",
                                        font=("TkFixedFont", 13))
        self.__difficulty_label.grid(row=0, column=0, pady=(0, 20))

        # Choose difficulty level
        self.__difficulties = {"radio_value": IntVar()}
        self.__difficulties["Easy"] = Radiobutton(self.__leftframe,
                                                  text="Easy", value=1,
                                                  variable=self.__difficulties[
                                                      "radio_value"])
        self.__difficulties["Medium"] = Radiobutton(self.__leftframe,
                                                    text="Medium", value=2,
                                                    variable=
                                                    self.__difficulties[
                                                        "radio_value"])
        self.__difficulties["Hard"] = Radiobutton(self.__leftframe,
                                                  text="Hard", value=3,
                                                  variable=self.__difficulties[
                                                      "radio_value"])
        self.__difficulties["Easy"].grid(row=1, column=0, sticky="W",
                                         padx=(20, 0))
        self.__difficulties["Medium"].grid(row=2, column=0, sticky="W",
                                           padx=(20, 0))
        self.__difficulties["Hard"].grid(row=3, column=0, sticky="W",
                                         padx=(20, 0), pady=(0, 50))

        # Start a new game
        self.__start_over = Button(self.__leftframe, text="Start game",
                                   font=("TkFixedFont", 10), width=10, pady=5,
                                   command=self.start_game)
        self.__start_over.grid(row=4, column=0, columnspan=4, pady=5)

        # Close the window
        self.__stop = Button(self.__leftframe, text="Quit game",
                             font=("TkFixedFont", 10), width=10, pady=5,
                             command=self.stop)
        self.__stop.grid(row=5, column=0, columnspan=4, pady=5)

        # Give instructions, will be updated to show if player won or not
        self.__game_outcome = Label(self.__rightframe,
                                    text="Select difficulty",
                                    font=("TkFixedFont", 15), width=50,
                                    background="white")
        self.__game_outcome.grid(row=0, column=0, columnspan=26, pady=10)

        # Keep score of how many games player has won
        self.__score_label = Label(self.__rightframe, text="Games won: 0",
                                   font=("TkFixedFont", 10), width=20,
                                   background="white")
        self.__score_label.grid(row=0, column=22, columnspan=26, pady=10)

        # Show underscores to represent length of the word, will be updated if
        # player guesses letter that are in the word.
        self.__guessed_word = Label(self.__rightframe,
                                    text="",
                                    font=("TkFixedFont", 16), width=50,
                                    background="white")
        self.__guessed_word.grid(row=1, column=0, columnspan=26, pady=10)

        # Show which letters have been guessed that were not in the word
        self.__guessed_letters = Label(self.__rightframe, text="",
                                       font=("TkFixedFont", 15), width=30,
                                       background="white")
        self.__guessed_letters.grid(row=3, column=0, columnspan=26)

        # Letter buttons. By pressing them guess if letter is in the
        # word or not.
        self.__letter_buttons = []

        column = 0
        for i, letter in enumerate(ascii_uppercase):
            self.__letter_buttons.append(
                Button(self.__rightframe, text=letter, width=2,
                       font=("TkFixedFont", 15), state=DISABLED,
                       command=lambda j=i: self.guess(j)))
            self.__letter_buttons[-1].grid(row=2, column=column, padx=3,
                                           pady=50)
            column += 1

        self.__letter_buttons[0].grid(padx=(15, 0))

        # Balloon images. Updated if guessed letter is not in the word.
        column = 7
        self.__balloon_images = []
        self.__balloon_labels = []
        self.__pop = PhotoImage(file="pop.GIF")
        for image_name in ["red.GIF", "orange.GIF", "yellow.GIF", "purple.GIF",
                           "blue.GIF", "green.GIF"]:
            self.__balloon_images.append(PhotoImage(file=image_name))

            self.__balloon_labels.append(
                Label(self.__rightframe, image=self.__balloon_images[-1],
                      highlightthickness=0, bd=0))
            self.__balloon_labels[-1].grid(row=5, column=column, columnspan=3)
            column += 2

    def start_window(self):
        """
        Open the window with the initialised elements.
        """
        self.__main_window.mainloop()

    def stop(self):
        """
        End the game by closing the window.
        """
        self.__main_window.destroy()

    def start_game(self):
        """
        Start a new game by preparing all the widgets of the game.
        """
        self.__balloons_left = 6
        self.__balloon_index = 0
        self.__letters_not_in_word = ""

        self.__guessed_letters.configure(text="")

        difficulty = self.get_difficulty()

        if difficulty in [1, 2, 3]:
            self.__difficulty_label.configure(foreground="black")
            self.__game_outcome.configure(
                text="Try to guess the word without popping all of the"
                     " balloons!")

            self.__word_to_be_guessed, under_scores = self.choose_word()

            self.__guessed_word.configure(text=under_scores)

            for i, letter in enumerate(ascii_uppercase):
                self.__letter_buttons[i].configure(text=letter, state=ACTIVE)

            for i, balloon in enumerate(self.__balloon_labels):
                balloon.configure(image=self.__balloon_images[i])

        else:
            self.__difficulty_label.configure(foreground="red")

    def guess(self, i):
        """
        Check if the guessed letter is in the word and make it visible if it
        is. Else pop one balloon. Check if the player won or lost.

        :param i: int, index number for list of letter buttons
        """
        letter = self.__letter_buttons[i].cget("text")
        word = self.__word_to_be_guessed
        guessed_word_so_far = list(self.__guessed_word.cget("text"))

        self.__letter_buttons[i].configure(text="", state=DISABLED)

        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    index = i
                    guessed_word_so_far[index] = letter
                    self.__guessed_word.configure(
                        text=''.join(guessed_word_so_far))

        else:
            self.__balloons_left -= 1

            self.__balloon_labels[self.__balloon_index].configure(
                image=self.__pop)
            self.__balloon_index += 1

            self.__letters_not_in_word += letter
            self.__guessed_letters.configure(
                text=f"Letters you have guessed: {self.__letters_not_in_word}")

        if self.__guessed_word.cget("text") == word:
            self.__score += 1
            self.__number_of_played_games += 1
            self.__score_label.configure(
                text=f"Games won: {self.__score} / "
                     f"{self.__number_of_played_games}")
            self.__game_outcome.configure(text="You won!")
            for button in range(len(self.__letter_buttons)):
                self.__letter_buttons[button].configure(state=DISABLED)

        if self.__balloons_left == 0:
            self.__number_of_played_games += 1
            self.__score_label.configure(
                text=f"Games won: {self.__score} / "
                     f"{self.__number_of_played_games}")
            self.__game_outcome.configure(text="You lost!")
            for button in range(len(self.__letter_buttons)):
                self.__letter_buttons[button].configure(state=DISABLED)
            self.__guessed_word.configure(text=word)

    def get_difficulty(self):
        return self.__difficulties["radio_value"].get()

    def choose_word(self):
        """
        Randomly choose a word to be guessed from a list of words.

        :return: str, the chosen word
        :return: str, underscores representing the amount of letters in the
                      word
        """
        easy = ['book', 'week', 'jazz', 'jump', 'cool', 'bear', 'cold', 'calm',
                'ball', 'date', 'cook', 'blue', 'wait']
        medium = ['jeans', 'ready', 'angry', 'winter', 'shear', 'orange',
                  'pickle', 'fluffy', 'violet', 'savory', 'honey', 'knife',
                  'scream']
        hard = ['relation', 'jellyfish', 'oatmeal', 'surprise', 'gorgeous',
                'avocado', 'aluminum', 'bathroom', 'precious', 'umbrella',
                'wednesday', 'dangerous', 'halloween', 'pineapple',
                'strawberry', 'entertaining']

        difficulty = self.get_difficulty()

        if difficulty == 1:
            word = choice(easy)
        elif difficulty == 2:
            word = choice(medium)
        else:
            word = choice(hard)

        word_with_spaces = ""

        for letter in word:
            word_with_spaces += letter
            word_with_spaces += " ".upper()

        word_with_spaces.replace(word_with_spaces[-1], "")

        under_scores = ""
        for letter in word_with_spaces:
            if letter != " ":
                under_scores += "_"
            else:
                under_scores += " "

        return word_with_spaces.upper(), under_scores


def main():
    ui = Userinterface()
    ui.start_window()


if __name__ == '__main__':
    main()
