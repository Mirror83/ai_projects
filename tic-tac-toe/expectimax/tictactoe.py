# Import the tkinter library with alias tk
import tkinter as tk
# Import the messagebox module from tkinter
from tkinter import messagebox
# Import the random module
import random

# Define a class for the Tic Tac Toe game
class TicTacToe:
    """
    Class to represent a Tic Tac Toe game.
    """

    # Constructor method to initialize the game
    def __init__(self):
        """
        Initialize the game.
        """
        # Initialize the Tkinter root window
        self.root = tk.Tk()
        # Set the title of the root window
        self.root.title("Tic Tac Toe")
        # Initialize a list to store buttons
        self.buttons = []
        # Initialize the board with empty spaces
        self.board = [' ']*9
        # Set the symbol for the player
        self.player = 'X'
        # Set the symbol for the opponent
        self.opponent = 'O'

        # Create buttons for the game grid
        for i in range(3):
            for j in range(3):
                # Create a button at position (i, j)
                button = tk.Button(self.root, text='', width=10, height=4, font=('Arial', 20),
                                   # Lambda function to pass the position (i*3+j) to make_move_and_update
                                   command=lambda i=i, j=j: self.make_move_and_update(i*3+j))
                # Place the button in the grid
                button.grid(row=i, column=j)
                # Add the button to the list of buttons
                self.buttons.append(button)

    # Method to make a move and update the game state
    def make_move_and_update(self, move):
        """
        Make a move and update the game state.
        """
        # Check if the chosen move is valid and the game is not over
        if self.board[move] == ' ' and not self.game_over():
            # Make the move for the player
            self.make_move(move, self.player)
            # Update the GUI board
            self.update_board()
            # Check if the game is over after the player's move
            if not self.game_over():
                # Make the best move for the opponent using the Expectimax algorithm
                self.make_best_move_expectimax()
                # Update the GUI board after the opponent's move
                self.update_board()
            # If the game is over after the opponent's move, show the result
            if self.game_over():
                self.show_result()

    # Method to update the GUI board
    def update_board(self):
        """
        Update the GUI board.
        """
        # Update the text of each button based on the current board state
        for i, button in enumerate(self.buttons):
            button.config(text=self.board[i])

    # Method to make a move on the board
    def make_move(self, move, player):
        """
        Make a move on the board.
        """
        # Set the chosen position on the board to the player's symbol
        self.board[move] = player

    # Method to get available moves on the board
    def available_moves(self):
        """
        Get available moves on the board.
        """
        # Return a list of indices where the board contains an empty space
        return [i for i in range(9) if self.board[i] == ' ']

    # Method to check if a player has won
    def check_winner(self, player):
        """
        Check if a player has won.
        """
        # Define winning combinations
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        # Check if any winning combination is achieved by the player
        for combination in winning_combinations:
            if all(self.board[i] == player for i in combination):
                return True
        return False

    # Method to check if the game is over
    def game_over(self):
        """
        Check if the game is over.
        """
        # Check if either player has won or if the board is full
        return self.check_winner(self.player) or self.check_winner(self.opponent) or ' ' not in self.board

    # Method to evaluate the game state
    def evaluate(self):
        """
        Evaluate the game state.
        """
        # If player wins, return 1; if opponent wins, return -1; if it's a tie, return 0
        if self.check_winner(self.player):
            return 1
        elif self.check_winner(self.opponent):
            return -1
        else:
            return 0

    # Method to perform expectimax search
    def expectimax(self, depth, player):
        """
        Perform expectimax search.
        """
        # Base case: if the game is over, return the evaluation of the current game state
        if self.game_over():
            return self.evaluate()

        if player == self.player:
            # Max player's turn
            best_score = float('-inf')
            # Iterate over available moves
            for move in self.available_moves():
                # Make the move for the player
                self.make_move(move, player)
                # Recursively call expectimax for the opponent
                score = self.expectimax(depth+1, self.opponent)
                # Undo the move
                self.make_move(move, ' ')
                # Update the best score
                best_score = max(score, best_score)
            return best_score
        else:
            # Chance node (opponent's turn)
            scores = []
            # Iterate over available moves
            for move in self.available_moves():
                # Make the move for the opponent
                self.make_move(move, player)
                # Recursively call expectimax for the player
                score = self.expectimax(depth+1, self.player)
                # Undo the move
                self.make_move(move, ' ')
                # Add the score to the list
                scores.append(score)
            # Calculate the average score
            return sum(scores) / len(scores)

    # Method to make the best move using expectimax
    def make_best_move_expectimax(self):
        """
        Make the best move using expectimax.
        """
        best_move = None
        best_average_score = float('-inf')
        # Iterate over available moves
        for move in self.available_moves():
            # Make the move for the opponent
            self.make_move(move, self.opponent)
            # Calculate the score using expectimax
            score = self.expectimax(0, self.player)
            # Undo the move
            self.make_move(move, ' ')
            # Update the best move and score
            if score > best_average_score:
                best_average_score= score
                best_move = move
        # Make the best move for the opponent
        self.make_move(best_move, self.opponent)

    # Method to show the game result
    def show_result(self):
        """
        Show the game result.
        """
        # Determine the game result and show a message box
        if self.check_winner(self.player):
            result = "You win!"
        elif self.check_winner(self.opponent):
            result = "You lose!"
        else:
            result = "It's a tie!"
        messagebox.showinfo("Game Over", result)

    # Method to run the game
    def run(self):
        """
        Run the game.
        """
        # Start the Tkinter event loop
        self.root.mainloop()

# Entry point of the program
if __name__ == "__main__":
    # Create a Tic Tac Toe game instance and run it
    game = TicTacToe()
    game.run()
