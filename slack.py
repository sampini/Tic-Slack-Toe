import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Slack app with the Bot Token and Signing Secret
app = App(token=os.getenv("SLACK_BOT_TOKEN"), signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

# Flask setup
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Tic-Tac-Toe game logic
class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_turn = 'X'
        self.game_over = False
    
    def display_board(self):
        board_str = ""
        for i in range(9):
            board_str += self.board[i] + ('|' if (i + 1) % 3 != 0 else '\n')
            if (i + 1) % 3 == 0 and i != 8:
                board_str += '-----\n'
        return board_str

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_turn
            if self.check_winner():
                self.game_over = True
                return f"{self.current_turn} wins!"
            elif ' ' not in self.board:
                self.game_over = True
                return "It's a tie!"
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return None
        else:
            return "Invalid move, try again."

    def check_winner(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for pos in winning_positions:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != ' ':
                return True
        return False

# Store only one game for the channel
game = None

@app.command("/start_game")
def start_game(ack, body, say):
    ack()
    global game
    if game and not game.game_over:
        say("A game is already in progress. Finish it before starting a new one.")
    else:
        game = TicTacToeGame()
        say(f"Tic-Tac-Toe game started!\n{game.display_board()}")

@app.command("/make_move")
def make_move(ack, body, say):
    ack()
    global game
    text = body['text']
    
    if not game:
        say("No active game. Use /start_game to start a new game.")
        return

    if game.game_over:
        say("The game is over. Start a new game with /start_game.")
        return

    try:
        position = int(text)
        if position < 0 or position > 8:
            say("Please enter a valid position (0-8).")
            return
    except ValueError:
        say("Please enter a valid position (0-8).")
        return

    result = game.make_move(position)
    board_display = game.display_board()
    if result:
        say(f"{result}\n{board_display}")
    else:
        say(f"Next move:\n{board_display}")

@app.command("/end_game")
def end_game(ack, body, say):
    ack()
    global game
    
    if not game:
        say("There is no active game to end.")
        return

    game = None
    say("The current game has been ended.")

# Flask route to handle Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Start Flask server for local development
if __name__ == "__main__":
    flask_app.run(port=3000)
