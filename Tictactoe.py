import random

class Board:
    def __init__(self):
        self.board = [" " for _ in range(9)]

    def print_board(self):
        for i in range(0, 9, 3):
            row = "|".join(str(j + 1) if self.board[j] == " " else self.board[j] for j in range(i, i + 3))
            print(row)
            if i < 6:
                print("-----")

    def is_valid_move(self, position):

        if 1 <= position <= 9:
            return self.board[position - 1] == " "
        return False

    def make_move(self, position, symbol):

        if self.is_valid_move(position):
            self.board[position - 1] = symbol
            return True
        return False

    def check_winner(self, symbol):

        # Check all winning conditions
        for i in range(3):
        # Check rows and columns
            if (
                self.board[i * 3]
                == self.board[i * 3 + 1]
                == self.board[i * 3 + 2]
                == symbol
            ) or (self.board[i] == self.board[i + 3] == self.board[i + 6] == symbol):
                return True
        # Check diagonals
        if (self.board[0] == self.board[4] == self.board[8] == symbol) or (
            self.board[2] == self.board[4] == self.board[6] == symbol
        ):
            return True
        return False

    def is_full(self):
        return all(cell != " " for cell in self.board)



class BasePlayer:
# all player applies 
    def __init__(self, symbol):
        """Initializes the player with a symbol."""
        self.symbol = symbol

    def make_move(self, board):
        pass


class HumanPlayer(BasePlayer):

    def make_move(self, board):

        try:
            position = int(input(f"Player {self.symbol}'s turn: "))
        except ValueError:
            return False
        return board.make_move(position, self.symbol)


class BotPlayer(BasePlayer):

    def make_move(self, board):

        valid_moves = [i + 1 for i in range(9) if board.is_valid_move(i + 1)]
        #print(f"Valid moves: {valid_moves}")
        position = random.choice(valid_moves)
        print(f"BotPlayer {self.symbol} 's turn: {position}")
        return board.make_move(position, self.symbol)


class Game:

    def __init__(self, player1, player2):
        """Initializes the game with two players."""
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def play(self):
        #run the game loop
        while True:
            self.board.print_board()
            if not self.current_player.make_move(self.board):
                print("Invalid move, try again.")
                continue

            if self.board.check_winner(self.current_player.symbol):
                self.board.print_board()
                print(f"Player {self.current_player.symbol} wins!")
                break

            if self.board.is_full():
                self.board.print_board()
                print("It's a tie!")
                break

            self.switch_player()


if __name__ == "__main__":
    # To play the game
    while True:
        num_human_players = input("How many human players? (1/2): ")
        if num_human_players in ["1", "2"]:
            break
        else:
            print("Please only enter 1 or 2.")

    player1 = HumanPlayer("X")
    player2 = BotPlayer("O")

    if num_human_players == "1":
        player2 = BotPlayer("O")
    elif num_human_players == "2":
        player2 = HumanPlayer("O")

    game = Game(player1, player2)
    game.play()

