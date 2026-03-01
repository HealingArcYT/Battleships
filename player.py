import board as b


class Player:
    canShoot: bool
    board: b.Board

    def __init__(self):
        self.board = b.Board(self)

    def shoot(self, x: int, y: int) -> bool:
        if not self.canShoot:
            return False

        if self.board.board[x][y].shot:
            return False

        self.board.board[x][y].shot = True
        return True