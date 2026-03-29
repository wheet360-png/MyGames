import numpy as np


class Player:
    def __init__(self, type):
        self.type = type
        self.input1 = 0
        self.waiting = True
        self.grid = np.full((10, 10), "_")
        self.firing_grid = np.full((10, 10), "_", dtype='U20')
        self.shipsplaced = []
        self.ships_lenlist = []
        self.ships_hit = []
        self.RED = "\033[31m"
        self.WHITE = "\033[37m"
        self.RESET = "\033[0m"
        if self.type == "1":
            self.opp_type = 2
        if self.type == "2":
            self.opp_type = 1
        self.shipsignore = []


        self.ship_type = {
            2: ("P", "Patrol Boat"),
            3: ("D", "Destroyer"),
            4: ("B", "Battleship"),
            5: ("A", "Aircraft Carrier")
        }

    def show_board(self, grid):
        # Print the header numbers
        print("    1   2   3   4   5   6   7   8   9   10")

        # Define row labels
        rows = "ABCDEFGHIJ"

        for i in range(10):
            # Start the line with the Letter (A, B, C...)
            row_str = f"{rows[i]} "

            # Loop through each column in that row
            for j in range(10):
                row_str += f"|_{grid[i, j]}_"

            # Close the last cell and print the row
            print(row_str + "|")

    def check_coords(self, input2):
        if len(input2) == 2 or len(input2) == 3:
            letter = input2[0]
            number = input2[1:]
            if letter.isalpha() and number.isdigit():
                row_val = letter.upper()
                col_val = int(number)
                if "A" <= row_val <= "J" and 1 <= col_val <= 10:
                    row_idx = ord(row_val) - ord("A")
                    col_idx = int(col_val) - 1
                    return row_idx, col_idx
                else:
                    print("Must be on the board")
                    return None, None
            else:
                print("Invalid input")
                return None, None
        else:
            print("Must be a coordinate")
            return None, None


    def place_ships(self):

        self.ships_lenlist = [2,3,3,4,5]
        waiting = True
        print(f"Player {self.type}, place your ships: ")


        while self.ships_lenlist:
            self.show_board(self.grid)
            end1_row, end1_col = None, None
            end2_row, end2_col = None, None

            while end1_row is None:
                coords = (input("Enter end of a ship: "))
                if coords.strip().lower() == "clear":
                    self.ships_lenlist = self.reset_grid()
                    self.ship_type[3] = ("D", "Destroyer")
                else:
                    end1_row, end1_col = self.check_coords(coords)

            while end2_row is None:
                coords = input("Enter the other end of a ship: ")
                if coords.strip().lower() == "clear":
                    self.ships_lenlist = self.reset_grid()
                    self.ship_type[3] = ("D", "Destroyer")
                else:
                    end2_row, end2_col = self.check_coords(coords)

            if not end1_row == end2_row or not end1_col == end2_col:
                if end1_row == end2_row:
                    start_col = min(end1_col, end2_col)
                    end_col = max(end1_col, end2_col)
                    ship_len = (end_col - start_col + 1)
                    if ship_len in self.ships_lenlist:
                            ship_slice = self.grid[end1_row, start_col : end_col + 1]
                            if len(ship_slice) == ship_len and np.all(ship_slice == "_"):
                                ship_slice[:] =  self.ship_type[ship_len][0]
                                if ship_len == 3:
                                    self.ship_type[3] = ("S", "Submarine")
                                self.ships_lenlist.remove(ship_len)
                            else:
                                print("The ship is on an invalid square")
                    else:
                        print("This ship has already been placed or is too long.")
                # column up and down ship
                elif end1_col == end2_col:
                    start_row = min(end1_row, end2_row)
                    end_row = max(end1_row, end2_row)
                    ship_len = (end_row - start_row + 1)
                    if ship_len in self.ships_lenlist:
                        ship_slice = self.grid[start_row: end_row + 1, end1_col]
                        if len(ship_slice) == ship_len and np.all(ship_slice == "_"):
                            ship_slice[:] = self.ship_type[ship_len][0]
                            if ship_len == 3:
                                self.ship_type[3] = ("S", "Submarine")
                            self.ships_lenlist.remove(ship_len)
                            print("Ships left: ", self.ships_lenlist)
                        else:
                            print("The ship is on an invalid square")
                    else:
                        print("This ship has already been placed or is too long.")
                else:
                    print("Must place a ship on a straight line")
            else:
                print("Ships must be longer than 1 square")



    def reset_grid(self):
        # Fills the entire 10x10 grid back with water
        self.grid.fill("_")
        self.show_board(self.grid)
        print(f"Board cleared! All ships available.")
        return [2, 3, 3, 4, 5]  # Returns a fresh list of ships

    def check_shipsunk(self):
        if self.ships_hit.count("A") == 5 and "A" not in self.shipsignore:
            self.shipsignore.append("A")
            return "Aircraft Carrier"
        elif self.ships_hit.count("B") == 4 and "B" not in self.shipsignore:
            self.shipsignore.append("B")
            return "Battleship"
        elif self.ships_hit.count("D") == 3 and "D" not in self.shipsignore:
            self.shipsignore.append("D")
            return "Destroyer"
        elif self.ships_hit.count("S") == 3 and "S" not in self.shipsignore:
            self.shipsignore.append("S")
            return "Submarine"
        elif self.ships_hit.count("P") == 2 and "P" not in self.shipsignore:
            self.shipsignore.append("P")
            return "Patrol Boat"
        else:
            return None

    def check_win(self):
        if len(self.ships_hit) == 17:
            return True
        else:
            return False

    def play_turn(self):
        while True:
            row, col = None, None
            while row is None:
                self.show_board(self.firing_grid)
                target = input(f"Player {self.opp_type}, select a target: ")
                row, col = self.check_coords(target)
            if self.firing_grid[row, col] == "_":
                if not self.grid[row, col] == "_":
                    self.firing_grid[row, col] = self.RED + "█" + self.RESET
                    self.ships_hit.append(self.grid[row, col])
                    self.show_board(self.firing_grid)
                    print("Hit")
                    return "H"
                else:
                    self.firing_grid[row, col] = self.WHITE + "█" + self.RESET
                    self.show_board(self.firing_grid)
                    print("Miss")
                    return None

            else:
                print("This square has already been fired at")
                continue


def wait(player):
    print(f"Pass the device to Player {player}")
    wait = input("Type anything to continue: ")

P1 = Player("1")
P2 = Player("2")

playing = True

P1.place_ships()
P1.show_board(P1.grid)
wait(2)
print("\n" * 40)
P2.place_ships()
P2.show_board(P2.grid)


while playing:
    wait(1)
    print("\n" * 40)
    while P2.play_turn() == "H":
        sunk = P2.check_shipsunk()
        if not sunk is None:
            print(f"You sunk an enemy {sunk}! ")
        if P2.check_win():
            print(f"Player 1 wins!")
            playing = False
            break
    if not playing:
        break
    wait(2)
    print("\n" * 40)
    while P1.play_turn() == "H":
        sunk = P1.check_shipsunk()
        if not sunk is None:
            print(f"You sunk an enemy {sunk}! ")
        if P1.check_win():
            print(f"Player 2 wins!")
            playing = False
            break