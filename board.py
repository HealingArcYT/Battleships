import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class Ship:
    x: int
    y: int
    length: int
    orientation: str
    def __init__(self, x: int, y: int, length: int, orientation: str):
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation


class Fieldstate:
    ship: bool
    shot: bool

    def __init__(self):
        self.ship = False
        self.shot = False



class Board:
    player: 'Player'
    board: list[list[Fieldstate]] = [[] for _ in range(10)]
    ships: list[Ship]
    def __init__(self, player: 'Player'):
        self.player = player
        for x in range(10):
            self.board[x] = [Fieldstate() for _ in range(10)]
        self.ships = []

    def place_ship(self, ship: Ship, x: int, y: int, orientation: str) -> bool:
        length = ship.length


        if ship in self.ships: # check if there is a change
            if ship.x == x and ship.y == y:
                if ship.orientation == orientation:
                    return True

            for i in range(ship.length): # remove old ship to prepare new ship
                if ship.orientation == "N":
                    self.board[ship.x + i][ship.y].ship = False

                if ship.orientation == "S":
                    self.board[ship.x - i][ship.y].ship = False

                if ship.orientation == "E":
                    self.board[ship.x][ship.y + i].ship = False

                if ship.orientation == "W":
                    self.board[ship.x][ship.y - i].ship = False


        # Count Number of ships of same size
        counter = 0
        for s in self.ships:
            if not s.length == length:
                continue

            if length == 4:
                return False

            counter += 1

        if length == 3:
            if counter > 2:
                return False

        if length == 2:
            if counter > 3:
                return False

        if length == 1:
            if counter > 4:
                return False


        if orientation not in ["N", "E", "S", "W"]: # wrong orientation
            return False


        if orientation == "N":
            if x + length > 9:
                return False

            """
            Checking for everything around the ship and at the ship itself follows this logic:
            [x - 1 + 0][y - 1] [x - 1 + 0][y] [x - 1 + 0][y + 1]
            [x - 1 + 1][y - 1] [x - 1 + 1][y] [x - 1 + 1][y + 1]
            [x - 1 + 2][y - 1] [x - 1 + 2][y] [x - 1 + 2][y + 1]
            ...
            
            I want to start one row above the vertical ship that goes from x, y downwards and check downwards
            so we count from 0 to length + 2 with i
            and check for [x - 1 + i][y -1], [x - 1 + i][y + 1] and [x - 1 + i][y]
            """

            for i in range(length + 2): # check with one field boundary for ships around
                if not 0 <= x - 1 + i <= 9:
                    continue

                if self.board[x - 1 + i][y].ship:
                    return False

                if y + 1 < 10:
                    if self.board[x - 1 + i][y + 1].ship:
                        return False

                if y - 1 >= 0:
                    if self.board[x - 1 + i][y - 1].ship:
                        return False

            if not ship in self.ships:
                self.ships += [ship]

            ship.x = x
            ship.y = y
            ship.orientation = orientation

            for i in range(length):
                self.board[x + i][y].ship = True

            return True


        if orientation == "S":
            if x - length < 0:
                return False

            """
            Checking for everything around the ship and at the ship itself follows this logic:
            
            ...
            [x + 1 - 2][y - 1] [x + 1 - 2][y] [x + 1 - 2][y + 1]
            [x + 1 - 1][y - 1] [x + 1 - 1][y] [x + 1 - 1][y + 1]
            [x + 1 - 0][y - 1] [x + 1 - 0][y] [x + 1 - 0][y + 1]

            I want to start one row below the vertical ship that goes from x, y upwards and check upwards
            so we count from 0 to length + 2 with i
            and check for [x + 1 - i][y - 1], [x + 1 - i][y + 1] and [x + 1 - i][y]
            """

            for i in range(length + 2): # check with one field boundary for ships around
                if not 0 <= x + 1 - i <= 9:
                    continue

                if self.board[x + 1 - i][y].ship:
                    return False

                if y + 1 < 10:
                    if self.board[x + 1 - i][y + 1].ship:
                        return False

                if y - 1 >= 0:
                    if self.board[x + 1 - i][y - 1].ship:
                        return False

            if not ship in self.ships:
                self.ships += [ship]

            ship.x = x
            ship.y = y
            ship.orientation = orientation

            for i in range(length):
                self.board[x - i][y].ship = True

            return True


        if orientation == "E":
            if y + length > 9:
                return False

            """
            Checking for everything around the ship and at the ship itself follows this logic:
            [x - 1][y - 1 + 0] [x - 1][y - 1 + 1] [x - 1][y - 1 + 2] ...
            [x    ][y - 1 + 0] [x    ][y - 1 + 1] [x    ][y - 1 + 2] ...
            [x + 1][y - 1 + 0] [x + 1][y - 1 + 1] [x + 1][y - 1 + 2] ...

            I want to start one column left of the horizontal ship that goes from x, y rightwards and check rightwards
            so we count from 0 to length + 2 with i
            and check for [x - 1][y - 1 + i], [x + 1][y - 1 + i], and [x][y - 1 + i]
            """

            for i in range(length + 2): # check with one field boundary for ships around
                if not 0 <= y - 1 + i <= 9:
                    continue

                if self.board[x][y - 1 + i].ship:
                    return False

                if x - 1 >= 0:
                    if self.board[x - 1][y - 1 + i].ship:
                        return False

                if x + 1 < 10:
                    if self.board[x + 1][y - 1 + i].ship:
                        return False

            if not ship in self.ships:
                self.ships += [ship]

            ship.x = x
            ship.y = y
            ship.orientation = orientation

            for i in range(length):
                self.board[x][y + i].ship = True

            return True


        if orientation == "W":
            if y - length < 0: # ship too long
                return False

            """
            Checking for everything around the ship and at the ship itself follows this logic:
            [x - 1][y + 1 - 2] [x - 1][y + 1 - 1] [x - 1][y + 1 - 0] ...
            [x    ][y + 1 - 2] [x    ][y + 1 - 1] [x    ][y + 1 - 0] ...
            [x + 1][y + 1 - 2] [x + 1][y + 1 - 1] [x + 1][y + 1 - 0] ...

            I want to start one column right of the horizontal ship that goes from x, y leftwards and check leftwards
            so we count from 0 to length + 2 with i
            and check for [x - 1][y + 1 - i], [x + 1][y + 1 - i], and [x][y + 1 - i]
            """

            for i in range(length + 2): # check with one field boundary for ships around
                if not 0 <= y + 1 - i <= 9:
                    continue

                if self.board[x][y + 1 - i].ship:
                    return False

                if x - 1 >= 0:
                    if self.board[x - 1][y + 1 - i].ship:
                        return False

                if x + 1 < 10:
                    if self.board[x + 1][y + 1 - i].ship:
                        return False

            if not ship in self.ships:
                self.ships += [ship]

            ship.x = x
            ship.y = y
            ship.orientation = orientation

            for i in range(length):
                self.board[x][y - i].ship = True

            return True

    def randomize_ships(self):
        ship_number_map = {1: 4, 2: 3, 3: 2, 4: 1}
        for length in range(1, 5):
            for i in range(ship_number_map[length]):
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(["N", "S", "E", "W"])
                ship = Ship(-1, -1, length, "")


                while not self.place_ship(ship, x, y, orientation):
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)
                    orientation = random.choice(["N", "S", "E", "W"])