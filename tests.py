import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from Tictactoe import Board,Game, HumanPlayer, BotPlayer


#1.The game is initialized with an empty board
class Test_initial_board_empty(unittest.TestCase):
    #if user input is "1" 
    @patch("builtins.input", side_effect=["1"])  
    def test_initial_empty_board(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = BotPlayer("O")

        def get_board_state():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                game = Game(player1, player2)
                return mock_stdout.getvalue()

        initial_board_state = get_board_state()

        # check  neither 'X' nor 'O' is present in the initial state of the board
        self.assertNotIn("X", initial_board_state)
        self.assertNotIn("O", initial_board_state)


#2.The game is initialized with either 2 players (human-human) or 1 player (human-bot)
class TestGameInitialization(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = MagicMock()

    @patch("builtins.input", side_effect=["1"])
    def test_game_initialized_with_1_player(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = BotPlayer("O")

        with patch("sys.stdout", self.mock_stdout):
            game = Game(player1, player2)

        # test the game is initialized with 1 player
        self.assertEqual(game.player1, player1)
        self.assertEqual(game.player2, player2)
        self.assertEqual(game.current_player, player1)

    @patch("builtins.input", side_effect=["2"])
    def test_game_initialized_with_2_players(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = HumanPlayer("O")

        with patch("sys.stdout", self.mock_stdout):
            game = Game(player1, player2)

        # test the game is initialized with 2 players
        self.assertEqual(game.player1, player1)
        self.assertEqual(game.player2, player2)
        self.assertEqual(game.current_player, player1)


#3.Players are assigned a unique piece to plays: X or O
class TestPlayerAssignment(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = MagicMock()

    @patch("builtins.input", side_effect=["1"])
    def test_players_assigned_unique_pieces(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = BotPlayer("O")

        with patch("sys.stdout", self.mock_stdout):
            game = Game(player1, player2)

        # Assert that players are assigned unique pieces
        self.assertEqual(player1.symbol, "X")
        self.assertEqual(player2.symbol, "O")
        self.assertNotEqual(player1.symbol, player2.symbol)


#4.After one player plays, the other player has a turn
class TestPlayerTurnSwitch(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_both_players_on_board_after_first_round(self, mock_stdout, mock_input):
        player1 = HumanPlayer("X")
        player2 = BotPlayer("O")

        game = Game(player1, player2)
        game.play()

        # Get the printed output
        printed_output = mock_stdout.getvalue()

        # Check if both 'O' and 'X' are present on the board after the first round
        self.assertIn('X', printed_output)
        self.assertIn('O', printed_output)

#5.All winning end of the games detected, and draw games are identified
#7.The correct game winner, if one exists, is detected
#wrote them together
class Result_correct(unittest.TestCase):

    #Test whether can find tie using 
    @patch("builtins.input", side_effect=["2", "1", "3", "5", "4", "6", "8", "7", "9"])
    def test_tie_detected(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = HumanPlayer("O")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            game = Game(player1, player2)
            game.play()

        # Extract the printed output
        printed_output = mock_stdout.getvalue()

        # Check if "It's a tie!" is present in the printed output
        self.assertIn("It's a tie!", printed_output)

    # Test whether can find winner
    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_win_detected(self, mock_input):
        player1 = HumanPlayer("X")
        player2 = HumanPlayer("O")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            game = Game(player1, player2)
            game.play()

        # Extract the printed output
        printed_output = mock_stdout.getvalue()

        # Check if "X wins" is present in the printed output
        self.assertIn("Player X wins!", printed_output)

#6.Players can play only in viable spots
class Test_viable_spot(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_invalid_move_same_spot(self):
        # Player 1 makes a move in position 1
        self.assertTrue(self.board.make_move(1, "X"))
        # Player 2 tries to make a move in the same position
        self.assertFalse(self.board.make_move(1, "O"))

    def test_valid_move_different_spots(self):
        # Player 1 makes a move in position 1
        self.assertTrue(self.board.make_move(1, "X"))
        # Player 2 makes a move in a different position
        self.assertTrue(self.board.make_move(2, "O"))

if __name__ == "__main__":
    unittest.main()
