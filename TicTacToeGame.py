class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_turn = 'X'
    
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
                return f"{self.current_turn} wins!"
            elif ' ' not in self.board:
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
