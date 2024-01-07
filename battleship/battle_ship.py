"""
Reetta koskinen

A battleship game.
"""

STARTING_BOARD = [[" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                  [0, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 0],
                  [1, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 1],
                  [2, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 2],
                  [3, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 3],
                  [4, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 4],
                  [5, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 5],
                  [6, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 6],
                  [7, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 7],
                  [8, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 8],
                  [9, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 9],
                  [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]]


class Ship:
    """
    Implements a ship in a battleship game that has a type and
    coordinates on the game board.
    """
    def __init__(self, ship_type, coordinates):
        """
        Constructor, initializes new objects.

        :param ship_type:str, name of the ship type
        :param coordinates: list, a list of the coordinates in the board that
                            a ship is located at
        """
        self.__ship_type = ship_type
        self.__coordinates = coordinates
        self.__guesses = []    # for checking if all of the coordinates of a ship have been guessed

    def got_hit(self, place_to_shoot):
        """
        Check if a ship in the game has the coordinates that the user guessed.

        :param place_to_shoot: str, guessed coordinates
        :return: bool, True if a ship got hit
        """
        return place_to_shoot in self.__coordinates

    def add_to_guesses(self, place_to_shoot):
        """
        Add guessed coordinates to a ship's list of guesses.

        :param place_to_shoot: str, guessed coordinates
        """
        self.__guesses.append(place_to_shoot)

    def is_defeated(self):
        """
        Check if all of a ships coordinates have been
        guessed and the ship is defeated.

        :return: bool, True if ship is defeated
        """
        return sorted(self.__guesses) == self.__coordinates

    def update_defeated_ship(self, board):
        """
        Update the game board with the defeated ships type at the ships
        coordinates. Tell the user what kind of a ship was sank.

        :param board: list, the game board
        """
        for coordinate in self.__coordinates:
            update_board(board, coordinate, self.__ship_type[0].upper())

        print(f"You sank a {self.__ship_type}!")


def game_won(ships):
    """
    Check if all of the ships in the game have been
    defeated and the game has been won.

    :param ships: list, all ships in the game
    :return: bool, True if all ships have been defeated
    """
    list_of_defeated_ships = []

    for ship in ships:
        list_of_defeated_ships.append(ship.is_defeated()) # for every ship add True to the list if the ship is defeated, False if not

    return all(list_of_defeated_ships)


def update_board(board, place_to_shoot=None, mark=" "):
    """
    Update the game board with the given mark at the guessed coordinates.

    :param board: list, the game board
    :param place_to_shoot: str, guessed coordinates
    :param mark: str, the mark to be drawn on the board
    :return: list, the game board after the updates
    """
    if place_to_shoot is not None:    # None is for printing the empty board at the start of the game
        column = ord(place_to_shoot[0]) - 64    # turn column letter from coordinates into a number for indexing the board
        row = int(place_to_shoot[1]) + 1
        board[row][column] = mark

    return board


def print_board(board):
    """
    Print the board on the screen.

    :param board: list, a matrix representing the board
    """
    print()
    for i in board:
        print(*i)
    print()


def shoot(board, ships, place_to_shoot):
    """
    Shoot at the board and update it with the correct mark depending on if the
    user hit a ship or not. If a ship was hit check if it was defeated.

    :param board: list, the game board
    :param ships: list, all ships in the game
    :param place_to_shoot: str, guessed coordinates
    """
    for ship in ships:
        if ship.got_hit(place_to_shoot):
            ship.add_to_guesses(place_to_shoot)
            if ship.is_defeated():
                ship.update_defeated_ship(board)
            else:
                update_board(board, place_to_shoot, "X")
            break    # if a ship was hit stop checking rest of the ships
        else:
            update_board(board, place_to_shoot, "*")


def is_not_valid_coord(coord):
    """
    Check if coordinates are in the correct form XY
    where X is a letter (column) and Y a number (row).

    :param coord: coordinates
    :return: bool, True if coordinates are not in the correct form
    """
    try:   # try is used for in case Y can not be converted to int
        if len(coord) != 2 or \
           coord[0] not in "ABCDEFGHIJ" or \
           int(coord[1]) not in range(10):
            raise ValueError
        else:
            return False

    except ValueError:
        return True


def read_file():
    """
    Read the file with the name that the user inputs and check if there is any
    errors in the file. If there is no errors save the information about the
    ships from the file into a list.

    :return: list, ships
    """
    filename = input("Enter file name: ")
    try:
        file = open(filename, mode="r")
    except OSError:
        print("File can not be read!")
        return

    overlapping_coordinates = []
    ships = []

    for line in file:    # split every line from the file into ship type and a list of coordinates
        line = line.strip()
        line = line.split(";")
        ship_type = line[0]
        line.remove(ship_type)
        coordinates = sorted(line)

        ships.append(Ship(ship_type,coordinates))    # add objectcts of the class Ship to the list of ships

        for coord in coordinates:    # Check if all coorninates in the file are in the correct form
            if is_not_valid_coord(coord):
                print("Error in ship coordinates!")
                return

            else:
                overlapping_coordinates.append(coord)    # if there are no errors save ship coordinates to a list

    for coordinates in overlapping_coordinates:    # check if there are overlapping coordinates in the list
        if overlapping_coordinates.count(coordinates) > 1:
            print("There are overlapping ships in the input file!")
            return

    file.close()
    return ships


def main():
    ships = read_file()

    do_loop = True
    if ships is None:    # don't do the loop if there was an error in reading the file
        do_loop = False

    guesses = []
    board = STARTING_BOARD    # for the first iteration of the loop the board is the empty starting board

    while do_loop:
        board = update_board(board)
        print_board(board)

        if game_won(ships):
            print("Congratulations! You sank all enemy ships.")
            do_loop = False

        else:
            place_to_shoot = input("Enter place to "
                                   "shoot (q to quit): ").upper()

            if place_to_shoot == "Q":
                print("Aborting game!")
                do_loop = False

            elif is_not_valid_coord(place_to_shoot):
                print("Invalid command!")

            elif place_to_shoot in guesses:
                print("Location has already been shot at!")

            else:   # if there are no errors in the input or the game doesn't end, shoot at the board
                guesses.append(place_to_shoot)
                shoot(board, ships, place_to_shoot)


if __name__ == '__main__':
    main()

