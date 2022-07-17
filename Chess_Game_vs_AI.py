import numpy as np
import random
import pygame as p

# some declarations and initializations for drawing the board
width = height = 512
square_dim = 8  # Since a chess board is 8 * 8
block_size = height // square_dim  # A Block (square) of board
Images = {}  # a dictionary to be used to draw the chess pieces on the board
FPS = 15

# Define each piece value, checkmate, depth
pieces_values = {"K": 99999, "Q": 90, "B": 30, "N": 30, "R": 50, "p": 10}
CHECKMATE_SCORE = 100000
MAX_DEPTH = 3
best_move = None
STALEMATE_SCORE = nodes_checked = w_draw = b_draw = 0

# PIECES SCORES ARRAYS FOR EVALUATION FUNCTION
b_knight_score = np.array([[-50, -10, -30, -30, -30, -30, -10, -50],
                           [-40, -20, 0, 5, 5, 0, -20, -40],
                           [-30, 5, 10, 15, 15, 10, 5, -30],
                           [-30, 0, 15, 20, 20, 15, 0, -30],
                           [-30, 5, 15, 20, 20, 15, 5, -30],
                           [-30, 0, 10, 15, 15, 10, 0, -30],
                           [-40, -20, 0, 0, 0, 0, -20, -40],
                           [-50, -10, -30, -30, -30, -30, -10, -50]])

w_knight_score = np.array([[-50, -10, -30, -30, -30, -30, -10, -50],
                           [-40, -20, 0, 0, 0, 0, -20, -40],
                           [-30, 0, 10, 15, 15, 10, 0, -30],
                           [-30, 5, 15, 20, 20, 15, 5, -30],
                           [-30, 0, 15, 20, 20, 15, 0, -30],
                           [-30, 5, 10, 15, 15, 10, 5, -30],
                           [-40, -20, 0, 5, 5, 0, -20, -40],
                           [-50, -10, -30, -30, -30, -30, -10, -50]])

b_bishop_score = np.array([[-20, -10, -10, -10, -10, -10, -10, -20],
                           [-10, 5, 0, 0, 0, 0, 5, -10],
                           [-10, 10, 10, 10, 10, 10, 10, -10],
                           [-10, 0, 10, 10, 10, 10, 0, -10],
                           [-10, 5, 5, 10, 10, 5, 5, -10],
                           [-10, 0, 5, 10, 10, 5, 0, -10],
                           [-10, 0, 0, 0, 0, 0, 0, -10],
                           [-20, -10, -10, -10, -10, -10, -10, -20]])

w_bishop_score = np.array([[-20, -10, -10, -10, -10, -10, -10, -20],
                           [-10, 0, 0, 0, 0, 0, 0, -10],
                           [-10, 0, 5, 10, 10, 5, 0, -10],
                           [-10, 5, 5, 10, 10, 5, 5, -10],
                           [-10, 0, 10, 10, 10, 10, 0, -10],
                           [-10, 10, 10, 10, 10, 10, 10, -10],
                           [-10, 5, 0, 0, 0, 0, 5, -10],
                           [-20, -10, -10, -10, -10, -10, -10, -20]])

queen_score = np.array([[-20, -10, -10, -5, -5, -10, -10, -20],
                        [-10, 0, 0, 0, 0, 0, 0, -10],
                        [-10, 5, 5, 5, 5, 5, 0, -10],
                        [0, 0, 5, 5, 5, 5, 0, -5],
                        [-5, 0, 5, 5, 5, 5, 0, -5],
                        [-10, 0, 5, 5, 5, 5, 0, -10],
                        [-10, 0, 0, 0, 0, 0, 0, -10],
                        [-20, -10, -10, -5, -5, -10, -10, -20]])

b_rook_score = np.array([[0, 0, 0, 5, 5, 0, 0, 0],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [5, 10, 10, 10, 10, 10, 10, 5],
                         [0, 0, 0, 0, 0, 0, 0, 0]])

w_rook_score = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                         [5, 10, 10, 10, 10, 10, 10, 5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [-5, 0, 0, 0, 0, 0, 0, -5],
                         [0, 0, 0, 5, 5, 0, 0, 0]])

b_king_score = np.array([[20, 30, 10, 0, 0, 10, 30, 20],
                         [20, 20, 0, 0, 0, 0, 20, 20],
                         [-10, -20, -20, -20, -20, -20, -20, -10],
                         [-20, -30, -30, -40, -40, -30, -30, -20],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30]])

w_king_score = np.array([[-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-30, -40, -40, -50, -50, -40, -40, -30],
                         [-20, -30, -30, -40, -40, -30, -30, -20],
                         [-10, -20, -20, -20, -20, -20, -20, -10],
                         [20, 20, 0, 0, 0, 0, 20, 20],
                         [20, 30, 10, 0, 0, 10, 30, 20]])

b_pawn_score = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                         [5, 10, 10, -20, -20, 10, 10, 5],
                         [5, -5, -10, 0, 0, -10, -5, 5],
                         [0, 0, 0, 20, 20, 0, 0, 0],
                         [5, 5, 10, 25, 25, 10, 5, 5],
                         [10, 10, 20, 30, 30, 20, 10, 10],
                         [50, 50, 50, 50, 50, 50, 50, 50],
                         [70, 70, 70, 70, 70, 70, 70, 70]])

w_pawn_score = np.array([[70, 70, 70, 70, 70, 70, 70, 70],
                         [50, 50, 50, 50, 50, 50, 50, 50],
                         [10, 10, 20, 30, 30, 20, 10, 10],
                         [5, 5, 10, 25, 25, 10, 5, 5],
                         [0, 0, 0, 20, 20, 0, 0, 0],
                         [5, -5, -10, 0, 0, -10, -5, 5],
                         [5, 10, 10, -20, -20, 10, 10, 5],
                         [0, 0, 0, 0, 0, 0, 0, 0]])


# Finds the best move there is after applying min_max
def find_best(chess, moves):
    global best_move, nodes_checked
    nodes_checked = 0
    best_move = None
    # random.shuffle(moves)

    if chess.white_turn:
        player_move = 1
    else:
        player_move = -1

    min_max(chess, moves, MAX_DEPTH, -CHECKMATE_SCORE, CHECKMATE_SCORE, player_move)

    print("Nodes Traversed:", nodes_checked)


def evaluate(chess):
    if chess.checkmate:
        if chess.white_turn:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE
    elif chess.stalemate:
        return STALEMATE_SCORE

    # unique, counts = np.unique(chess.board, return_counts=True)
    # pc = dict(zip(unique, counts))

    # material = 100 * (pc['wp'] - pc['bp']) + 320 * (pc['wN'] - pc['bN']) + 330 * (pc['wB'] - pc['bB']) + 500 * (pc[
    # 'wR'] - pc['bR']) + 900 * (pc['wQ'] - pc['bQ'])

    score = 0
    for row in range(len(chess.board)):
        for col in range(len(chess.board[row])):
            sq = chess.board[row][col]
            if sq != "--":
                temp_score = 0
                if sq == "wp":
                    temp_score = w_pawn_score[row][col]
                elif sq == "bp":
                    temp_score = b_pawn_score[row][col]

                elif sq == "bK":
                    temp_score = b_king_score[row][col]
                elif sq == "wK":
                    temp_score = w_king_score[row][col]

                elif sq[1] == 'Q':
                    temp_score = queen_score[row][col]

                elif sq == "wB":
                    temp_score = w_bishop_score[row][col]
                elif sq == "bB":
                    temp_score = b_bishop_score[row][col]

                elif sq == "bR":
                    temp_score = b_rook_score[row][col]
                elif sq == "wR":
                    temp_score = w_rook_score[row][col]

                elif sq == "bN":
                    temp_score = b_knight_score[row][col]
                elif sq == "wN":
                    temp_score = w_knight_score[row][col]

                if sq[0] == 'w':
                    score += pieces_values[sq[1]] + temp_score * .1
                elif sq[0] == 'b':
                    score -= pieces_values[sq[1]] + temp_score * .1

    return score


# Nega_Max
def min_max(chess, moves, depth, alpha, beta, player_move):
    global best_move, nodes_checked
    nodes_checked += 1
    if depth == 0:
        return player_move * evaluate(chess)

    max_score = -CHECKMATE_SCORE
    for move in moves:

        pos = [move.start, move.end]
        chess.move_piece(pos, moves, False)
        next_moves = chess.valid_moves()
        score = -min_max(chess, next_moves, depth - 1, -beta, -alpha, -player_move)
        if score > max_score:
            max_score = score
            if depth == MAX_DEPTH:
                best_move = move
        chess.undo()

        # Alpha-Beta Pruning
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


# Keep track of moves, pieces killed
class Move:
    def __init__(self, start, end, kill_piece, check_castle_move=False):
        self.start = start
        self.end = end
        self.piece = (start[0], start[1])
        self.kill_piece = kill_piece
        self.check_castle_move = check_castle_move

    def __repr__(self):
        return '({0})'.format(self.end)

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented

        return self.end == other.end and self.piece == other.piece and self.start == other.start


# Checks if castling is allowed or not
class Castling:
    def __init__(self, w_king, b_king, w_queen, b_queen):
        self.w_king = w_king
        self.b_king = b_king
        self.w_queen = w_queen
        self.b_queen = b_queen


class Chess:
    # Numbering the board
    row_index = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    col_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_row = {v: k for k, v in row_index.items()}
    index_col = {v: k for k, v in col_index.items()}

    # Defining variables needed
    def __init__(self, board):
        self.board = board
        self.white_turn = True
        self.in_check = False
        self.checkmate = False
        self.stalemate = False
        self.w_king_loc = (7, 4)
        self.b_king_loc = (0, 4)
        self.checks = []
        self.pins = []
        self.log = []
        self.current_castle = Castling(True, True, True, True)
        self.caste_logs = [Castling(self.current_castle.w_king, self.current_castle.b_king,
                                    self.current_castle.w_queen, self.current_castle.b_queen)]

    def check_castle_mate(self, row, col):
        self.white_turn = not self.white_turn
        opp_moves = self.all_moves()
        self.white_turn = not self.white_turn
        for move in opp_moves:
            if move.end[0] == row and move.end[1] == col:
                return True

        return False

    def is_castle_valid(self, pos, killed):

        # Check if Rook Moved or Killed
        if (self.board[pos[1][0]][pos[1][1]] == "wR") or killed:
            if pos[0][0] == 7:
                if pos[0][1] == 0:
                    self.current_castle.w_queen = False
                elif pos[0][1] == 7:
                    self.current_castle.w_king = False
        elif (self.board[pos[1][0]][pos[1][1]] == "bR") or killed:
            if pos[0][0] == 0:
                if pos[0][1] == 0:
                    self.current_castle.b_queen = False
                elif pos[0][1] == 7:
                    self.current_castle.b_king = False
        # Check if King Moved
        elif self.board[pos[1][0]][pos[1][1]] == "wK":
            self.current_castle.w_king = False
            self.current_castle.w_queen = False
        elif self.board[pos[1][0]][pos[1][1]] == "bK":
            self.current_castle.b_king = False
            self.current_castle.b_queen = False

    def undo(self):
        if len(self.log) != 0:
            temp = self.log.pop()
            pos = temp[0]
            captured = temp[2]
            old_piece = temp[1]
            test = temp[3]

            self.board[pos[1][0]][pos[1][1]] = captured
            self.board[pos[0][0]][pos[0][1]] = old_piece
            self.white_turn = not self.white_turn
            if old_piece == 'wK':
                self.w_king_loc = (pos[0][0], pos[0][1])
            elif old_piece == 'bK':
                self.b_king_loc = (pos[0][0], pos[0][1])

            self.caste_logs.pop()
            new = self.caste_logs[-1]
            self.current_castle = Castling(new.w_king, new.b_king, new.w_queen, new.b_queen)
            if test:
                if pos[1][1] - pos[0][1] == 2:
                    self.board[pos[1][0]][pos[1][1] + 1] = self.board[pos[1][0]][pos[1][1] - 1]
                    self.board[pos[1][0]][pos[1][1] - 1] = "--"
                else:
                    self.board[pos[1][0]][pos[1][1] - 2] = self.board[pos[1][0]][pos[1][1] + 1]
                    self.board[pos[1][0]][pos[1][1] + 1] = "--"

    def castling_moves(self, pos, moves):
        row = pos[0]
        col = pos[1]

        if self.in_check:
            return

        # Check if squared empty and not in check, right side
        if (self.white_turn and self.current_castle.w_king) or (not self.white_turn and self.current_castle.b_king):
            if self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--":
                if not self.check_castle_mate(row, col + 1) and not self.check_castle_mate(row, col + 2):
                    moves.append(Move((row, col), (row, col + 2), False, check_castle_move=True))

        # Check if squared empty and not in check, left side
        if (self.white_turn and self.current_castle.w_queen) or (not self.white_turn and self.current_castle.b_queen):
            if self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" \
                    and self.board[row][col - 3] == "--":
                if not self.check_castle_mate(row, col - 1) and not self.check_castle_mate(row, col - 2):
                    moves.append(Move((row, col), (row, col - 2), False, check_castle_move=True))

    def queen_moves(self, pos, moves):
        self.bishop_moves(pos, moves)
        self.rook_moves(pos, moves)

    def king_moves(self, pos, moves):
        row = pos[0]
        col = pos[1]
        current_player = "w" if self.white_turn else "b"

        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for i in range(len(self.board)):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                endPiece = self.board[end_row][end_col]
                # If is something other then same color piece
                if endPiece[0] != current_player:
                    # place king on the end square and check for checks
                    if current_player == "w":
                        self.w_king_loc = (end_row, end_col)
                    else:
                        self.b_king_loc = (end_row, end_col)
                    in_check, pins, checks = self.find_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), False))
                    # Placing King Back on original Position
                    if current_player == "w":
                        self.w_king_loc = (row, col)
                    else:
                        self.b_king_loc = (row, col)

    def knight_moves(self, pos, moves):
        row = pos[0]
        col = pos[1]
        pinned_sq = False
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        current_player = "w" if self.white_turn else "b"

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                pinned_sq = True
                self.pins.remove(self.pins[i])
                break
                
        for move in knightMoves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not pinned_sq:
                    endPiece = self.board[end_row][end_col]
                    # If to Move Location is Not an Same Color piece
                    if endPiece[0] != current_player:
                        if endPiece == "--":
                            moves.append(Move((row, col), (end_row, end_col), False))
                        else:
                            moves.append(Move((row, col), (end_row, end_col), True))

    def bishop_moves(self, pos, moves):
        row = pos[0]
        col = pos[1]

        bishopMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        opponent = "b" if self.white_turn else "w"

        pinned_sq = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                pinned_sq = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        for piece_range in bishopMoves:
            for i in range(1, len(self.board)):
                end_row = row + piece_range[0] * i
                end_col = col + piece_range[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not pinned_sq or pin_direction == piece_range or pin_direction == (-piece_range[0], -piece_range[1]):
                        endPiece = self.board[end_row][end_col]
                        # if its Empty Space
                        if endPiece == "--":
                            moves.append(Move((row, col), (end_row, end_col), False))
                        # if its the enemy Piece
                        elif endPiece[0] == opponent:
                            moves.append(Move((row, col), (end_row, end_col), True))
                            break
                        # if its same color piece
                        else:
                            break
                # if its Off the Board move
                else:
                    break

    def rook_moves(self, pos, moves):
        row = pos[0]
        col = pos[1]
        rookMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))
        opponent = "b" if self.white_turn else "w"

        pinned_sq = False
        pinned_sq_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                pinned_sq = True
                pinned_sq_dir = (self.pins[i][2], self.pins[i][3])
                # Check Here for Rook
                # Rook Cant Remove Queen
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
                
        for piece_range in rookMoves:
            for i in range(1, len(self.board)):
                end_row = row + piece_range[0] * i
                end_col = col + piece_range[1] * i
                # check if Move not off Board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not pinned_sq or pinned_sq_dir == piece_range or pinned_sq_dir == (-piece_range[0], -piece_range[1]):
                        endPiece = self.board[end_row][end_col]
                        # check if Empty Space Valid
                        if endPiece == "--":
                            moves.append(Move((row, col), (end_row, end_col), False))
                        # if its the enemy piece on Move Location
                        elif endPiece[0] == opponent:
                            moves.append(Move((row, col), (end_row, end_col), True))
                            break
                        # if piece of same color then
                        else:
                            break
                # This is if Move was out of Bound/Board
                else:
                    break

    def pawn_moves(self, pos, moves):

        row = pos[0]
        col = pos[1]

        pinned_sq = False
        pinned_sq_dir = ()
        # Check if piece pinned/in check
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                pinned_sq = True
                pinned_sq_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # White Pawn Moves
        if self.white_turn:
            # Forward Moves
            if self.board[row - 1][col] == "--":
                if not pinned_sq or pinned_sq_dir == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), False))
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), False))

            # Right Diagonal Kill Option
            if col + 1 <= len(self.board) - 1:
                if self.board[row - 1][col + 1][0] == 'b':
                    if not pinned_sq or pinned_sq_dir == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), True))

            # Left Diagonal Kill Option
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    if not pinned_sq or pinned_sq_dir == (-1, -1):
                        moves.append(Move((row, col), (row - 1, col - 1), True))

        # Black Pawn Moves
        else:
            # Forward Moves
            if self.board[row + 1][col] == "--":
                if not pinned_sq or pinned_sq_dir == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), False))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), False))

            # Right Diagonal Kill Option
            if col + 1 <= len(self.board) - 1:
                if self.board[row + 1][col + 1][0] == 'w':
                    if not pinned_sq or pinned_sq_dir == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), True))

            # Left Diagonal Kill Option
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if not pinned_sq or pinned_sq_dir == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), True))

    def move_piece(self, pos, moves, actual):
        global w_draw, b_draw
        # pos[0] = row, col of current position
        # pos[1] = row, col of position of move to make
        test = Move(pos[0], pos[1], False)
        for move in moves:
            if test == move:
                test.check_castle_move = move.check_castle_move
                break

        if self.board[pos[1][0]][pos[1][1]] == "--":
            killed = False
        else:
            killed = True

        if test in moves:
            old_pos = self.board[pos[0][0]][pos[0][1]]
            new_pos = self.board[pos[1][0]][pos[1][1]]

            self.board[pos[1][0]][pos[1][1]] = self.board[pos[0][0]][pos[0][1]]
            self.board[pos[0][0]][pos[0][1]] = "--"

            temp = [pos, old_pos, new_pos, test.check_castle_move]
            self.log.append(temp)

            new_pos = self.board[pos[1][0]][pos[1][1]]

            self.white_turn = not self.white_turn

            # Keep track of King position for pins/checks
            if new_pos == "wK":
                self.w_king_loc = (pos[1][0], pos[1][1])
            elif new_pos == "bK":
                self.b_king_loc = (pos[1][0], pos[1][1])

            # If pawn reaches end
            if (new_pos == "wp" and pos[1][0] == 0) or (new_pos == "bp" and pos[1][0] == 7):
                if actual:
                    new_inp = input("Promote pawn to: ('R', 'N', 'B', 'Q')")
                    self.board[pos[1][0]][pos[1][1]] = new_pos[0] + new_inp
                else:
                    self.board[pos[1][0]][pos[1][1]] = new_pos[0] + 'Q'

            if test.check_castle_move:
                if pos[1][1] - pos[0][1] == 2:
                    self.board[pos[1][0]][pos[1][1] - 1] = self.board[pos[1][0]][pos[1][1] + 1]
                    self.board[pos[1][0]][pos[1][1] + 1] = "--"
                else:
                    self.board[pos[1][0]][pos[1][1] + 1] = self.board[pos[1][0]][pos[1][1] - 2]
                    self.board[pos[1][0]][pos[1][1] - 2] = "--"

            self.is_castle_valid(pos, killed)
            self.caste_logs.append(Castling(self.current_castle.w_king, self.current_castle.b_king,
                                            self.current_castle.w_queen, self.current_castle.b_queen))

            if actual:
                if self.white_turn:
                    if killed:
                        w_draw = 0
                    else:
                        w_draw += 1
                else:
                    if killed:
                        b_draw = 0
                    else:
                        b_draw += 1

            return old_pos + " " + self.index_col[pos[0][1]] + self.index_row[pos[0][0]] + "," + self.index_col[
                pos[1][1]] + self.index_row[pos[1][0]]

        return "Invalid Move"

    def all_moves(self):

        # Get all possible moves of player at current board
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                pos = (row, col)
                player = self.board[row][col][0]
                if (player == 'w' and self.white_turn) or (player == 'b' and not self.white_turn):
                    piece = self.board[row][col][1]

                    if piece == 'K':
                        self.king_moves(pos, moves)
                    elif piece == 'Q':
                        self.queen_moves(pos, moves)
                    elif piece == 'R':
                        self.rook_moves(pos, moves)
                    elif piece == 'B':
                        self.bishop_moves(pos, moves)
                    elif piece == 'N':
                        self.knight_moves(pos, moves)
                    elif piece == 'p':
                        self.pawn_moves(pos, moves)

        return moves
    
    def valid_moves(self):

        moves = []
        temp = Castling(self.current_castle.w_king, self.current_castle.b_king,
                        self.current_castle.w_queen, self.current_castle.b_queen)

        self.in_check, self.pins, self.checks = self.find_checks()
        opponent, player, king_row, king_col = self.get_colour_location()

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.all_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_check = self.board[check_row][check_col]
                valid_sq = []
                if piece_check[1] == 'N':
                    valid_sq = [(check_row, check_col)]
                else:
                    for i in range(1, len(self.board)):
                        valid_sqr = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_sq.append(valid_sqr)
                        if valid_sqr[0] == check_row and valid_sqr[1] == check_col:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if self.board[moves[i].start[0]][moves[i].start[1]][1] != 'K':
                        if not (moves[i].end[0], moves[i].end[1]) in valid_sq:
                            moves.remove(moves[i])

            else:
                self.king_moves((king_row, king_col), moves)
        else:
            moves = self.all_moves()

        if self.white_turn:
            self.castling_moves((self.w_king_loc[0], self.w_king_loc[1]), moves)
        else:
            self.castling_moves((self.b_king_loc[0], self.b_king_loc[1]), moves)

        self.current_castle = temp
        return moves

    def get_colour_location(self):
        if self.white_turn:
            opponent = "b"
            player = "w"
            king_row = self.w_king_loc[0]
            king_col = self.w_king_loc[1]
        else:
            opponent = "w"
            player = "b"
            king_row = self.b_king_loc[0]
            king_col = self.b_king_loc[1]

        return opponent, player, king_row, king_col

    def find_checks(self):
        pins = []
        checks = []
        in_check = False
        opponent, player, king_row, king_col = self.get_colour_location()

        # Knights Check
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knightMoves:
            end_r = king_row + move[0]
            end_c = king_col + move[1]
            if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board):
                end_piece = self.board[end_r][end_c]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_r, end_c, move[0], move[1]))

        # Other pieces checks
        check_side = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(check_side)):
            piece_range = check_side[j]
            is_pin_possible = ()
            for i in range(1, len(self.board)):
                end_r = king_row + piece_range[0] * i
                end_c = king_col + piece_range[1] * i
                if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board):
                    end_piece = self.board[end_r][end_c]
                    if end_piece[0] == player:
                        if is_pin_possible == ():
                            is_pin_possible = (end_r, end_c, piece_range[0], piece_range[1])
                        else:
                            break
                    elif end_piece[0] == opponent:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or (4 <= j <= 7 and piece_type == 'B') or (
                                i == 1 and piece_type == 'p' and (
                                (opponent == 'w' and 6 <= j <= 7) or (opponent == 'b' and 4 <= j <= 5))) or (
                                piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if is_pin_possible == ():
                                in_check = True
                                checks.append((end_r, end_c, piece_range[0], piece_range[1]))
                                break
                            else:
                                pins.append(is_pin_possible)
                                break
                        else:
                            break
                else:
                    break

        return in_check, pins, checks


# Get random Move
def findRandomMove(Moves):
    position = random.choice(Moves)
    return position


# Check Game Over
def end_game(length, gameplay, chess):
    if length == 0:
        if chess.in_check:
            chess.checkmate = True
        else:
            chess.stalemate = True

    if chess.checkmate:
        if chess.white_turn:
            print("Black Wins")
        else:
            print("White Wins")
        gameplay = False
    elif chess.stalemate:
        print("Draw")
        gameplay = False

    return gameplay


# A Function to Load the Images from the local Storage Folder images
def get_images():
    pieces = ['wp', 'wK', 'wQ', 'wB', 'wN', 'wR', 'bp', 'bK', 'bQ', 'bB', 'bN',
              'bR']  # an array with names of all pieces
    for piece in pieces:
        # Loading the image using the pygame library  built in function
        Images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (block_size, block_size))
        # This allow us accessing an image by Images["piece_name"]


# this function draws the board grey and white blocks
def print_board(screen):
    colours = [p.Color("snow"), p.Color("lightskyblue")]
    for i in range(square_dim):
        for j in range(square_dim):
            color = colours[(i + j) % 2]
            p.draw.rect(screen, color, p.Rect(j * block_size, i * block_size, block_size, block_size))


# This function draws the pieces on top of the Board Drawn
def print_pieces(screen, board):
    for i in range(square_dim):
        for j in range(square_dim):
            piece = board[i][j]
            if piece != "--":  # that its not an empty space but contains a piece then
                screen.blit(Images[piece], p.Rect(j * block_size, i * block_size, block_size, block_size))


# Draw the board and pieces
def print_game(screen, board):
    # This function utilizes the above two functions and make the chess board
    print_board(screen)
    print_pieces(screen, board)


def main():
    board = np.array([
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ])

    global best_move, b_draw, w_draw
    chess = Chess(board)
    
    # Set player / AI
    white_player = True
    black_player = False
    
    incorrect = False
    gameplay = True

    p.init()
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("white"))
    clock = p.time.Clock()
    get_images()
    selectedBlock = ()  # this helps keep track of last click of user
    last2Clicks = []  # keeps last two clicks

    while gameplay:
        for e in p.event.get():
            if e.type == p.QUIT:
                gameplay = False

            # If both player playing
            if white_player and black_player:

                print_game(screen, board)
                clock.tick(FPS)
                p.display.flip()

                moves = chess.valid_moves()
                # print(moves)
                gameplay = end_game(len(moves), gameplay, chess)

                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # gets location of mouse
                    col = location[0] // block_size
                    row = location[1] // block_size
                    # print(row, col)
                    if selectedBlock == (row, col):  # that is the user clicked same  block twice
                        selectedBlock = ()
                        last2Clicks = []
                    else:
                        selectedBlock = (row, col)
                        last2Clicks.append(selectedBlock)
                    if len(last2Clicks) == 2:

                        st_row = last2Clicks[0][0]
                        st_col = last2Clicks[0][1]
                        e_row = last2Clicks[1][0]
                        e_col = last2Clicks[1][1]
                        # print(last2Clicks)
                        # print(moves)

                        pos = [(st_row, st_col), (e_row, e_col)]

                        new_pos = chess.move_piece(pos, moves, True)

                        print(new_pos)
                        selectedBlock = ()
                        last2Clicks = []
            # If white player and black AI
            elif white_player and not black_player:

                print_game(screen, board)
                clock.tick(FPS)
                p.display.flip()

                moves = chess.valid_moves()
                # print(moves)
                gameplay = end_game(len(moves), gameplay, chess)

                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # gets location of mouse
                    col = location[0] // block_size
                    row = location[1] // block_size
                    # print(row, col)
                    if selectedBlock == (row, col):  # that is the user clicked same  block twice
                        selectedBlock = ()
                        last2Clicks = []
                    else:
                        selectedBlock = (row, col)
                        last2Clicks.append(selectedBlock)
                    if len(last2Clicks) == 2:

                        st_row = last2Clicks[0][0]
                        st_col = last2Clicks[0][1]
                        e_row = last2Clicks[1][0]
                        e_col = last2Clicks[1][1]
                        # print(last2Clicks)

                        pos = [(st_row, st_col), (e_row, e_col)]

                        new_pos = chess.move_piece(pos, moves, True)

                        if new_pos == "Invalid Move":
                            print("Invalid Move.")
                            selectedBlock = ()
                            last2Clicks = []
                            continue

                        print(new_pos)
                        print_game(screen, board)
                        clock.tick(FPS)
                        p.display.flip()

                        moves = chess.valid_moves()

                        gameplay = end_game(len(moves), gameplay, chess)

                        find_best(chess, moves)
                        if best_move is None:
                            best_move = findRandomMove(moves)

                        pos = [best_move.start, best_move.end]

                        new_pos = chess.move_piece(pos, moves, True)

                        if new_pos == "Draw":
                            print("Draw (50 moves)")
                            gameplay = False

                        print(new_pos)
                        selectedBlock = ()
                        last2Clicks = []

            # If black player and white AI
            elif black_player and not white_player:

                if not incorrect:
                    incorrect = True
                    moves = chess.valid_moves()

                    gameplay = end_game(len(moves), gameplay, chess)

                    find_best(chess, moves)
                    if best_move is None:
                        best_move = findRandomMove(moves)

                    pos = [best_move.start, best_move.end]

                    new_pos = chess.move_piece(pos, moves, True)
                    if new_pos == "Draw":
                        print("Draw (50 moves)")
                        gameplay = False
                    print(new_pos)

                    print_game(screen, board)
                    clock.tick(FPS)
                    p.display.flip()

                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # gets location of mouse
                    col = location[0] // block_size
                    row = location[1] // block_size
                    # print(row, col)
                    if selectedBlock == (row, col):  # that is the user clicked same  block twice
                        selectedBlock = ()
                        last2Clicks = []
                    else:
                        selectedBlock = (row, col)
                        last2Clicks.append(selectedBlock)
                    if len(last2Clicks) == 2:

                        moves = chess.valid_moves()

                        gameplay = end_game(len(moves), gameplay, chess)

                        st_row = last2Clicks[0][0]
                        st_col = last2Clicks[0][1]
                        e_row = last2Clicks[1][0]
                        e_col = last2Clicks[1][1]

                        pos = [(st_row, st_col), (e_row, e_col)]

                        new_pos = chess.move_piece(pos, moves, True)

                        if new_pos == "Invalid Move":
                            print("Invalid Move.")
                            selectedBlock = ()
                            last2Clicks = []
                            incorrect = True
                            continue

                        print(new_pos)
                        print_game(screen, board)
                        clock.tick(FPS)
                        p.display.flip()

                        selectedBlock = ()
                        last2Clicks = []
                        incorrect = False
            # If both AI
            elif not white_player and not black_player:

                moves = chess.valid_moves()

                gameplay = end_game(len(moves), gameplay, chess)

                find_best(chess, moves)
                if best_move is None:
                    best_move = findRandomMove(moves)

                pos = [best_move.start, best_move.end]

                new_pos = chess.move_piece(pos, moves, True)

                if new_pos == "Draw":
                    print("Draw (50 moves)")
                    gameplay = False

                print(new_pos)
                print_game(screen, board)
                clock.tick(FPS)
                p.display.flip()

    gameplay = True
    while gameplay:
        for e in p.event.get():
            if e.type == p.QUIT:
                gameplay = False

        print_game(screen, board)
        clock.tick(FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
