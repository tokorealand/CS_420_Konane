# Game Board requires height and width dimensions.
from piece import *
import random
from copy import deepcopy

"""
GameBoard has been to designed to work with 6x6 or 8x8 boards.
Other formats are not guaranteed nor expected to work.
"""


class gameBoard():
    WHITE = -1  # piece value
    BLACK = 1  # piece value
    STILLPLAYING = 0
    BLACKWON = 1
    WHITEWON = -1
    BLACK_ICON = "B"  # black symb
    WHITE_ICON = "W"  # white symb

    # Adds a game piece to the board and the relevant players piece list
    def add_piece(self, color, value, x, y):
        current_piece = gamePiece(color, value, x, y)

        if color == gameBoard.BLACK_ICON:
            self.total_pieces[current_piece.x][current_piece.y] = current_piece
            self.black_pieces[current_piece.piece_id] = current_piece
        else:
            self.total_pieces[current_piece.x][current_piece.y] = current_piece
            self.white_pieces[current_piece.piece_id] = current_piece
        return color

    # Moves the pieces around/removes them one a move is inputted
    def update_game_piece_position(self, x1, y1, x2, y2):
        if not (x2 == None and y2 == None):
            self.last_move = "[" + str(x1) + "," + str(y1) + "]" + " to " + "[" + str(x2) + "," + str(
                y2) + "]" + "piece color: " + self.total_pieces[x1][y1].color
            self.total_pieces[x2][y2] = self.total_pieces[x1][y1]
            self.total_pieces[x2][y2].update_coordinates(x2, y2)
            self.total_pieces[x1][y1] = "-"
        else:
            self.last_move = "Removed [" + str(x1 + 1) + "," + str(y1 + 1) + "]" + " piece color: " + \
                             self.total_pieces[x1][
                                 y1].color
            piece_to_remove = self.total_pieces[x1][y1]
            if piece_to_remove.color == gameBoard.BLACK_ICON:
                del self.black_pieces[piece_to_remove.piece_id]  # deletes the piece from the player's piece list
            else:
                del self.white_pieces[piece_to_remove.piece_id]  # deletes the piece from the player's piece list
            self.total_pieces[x1][y1] = "-"

    def __init__(self, height, width):
        """
        Constructs a board with given dimensions and sets the initial player turn ordering.
        """

        self.width = width
        self.height = height
        self.turn = 0
        self.total_pieces = [[" " for x in range(width)] for y in range(width)]
        self.black_pieces = {}
        self.white_pieces = {}
        self.last_move = "No moves"  # Used for printing to the GUI
        self.draw_board(width, height)  # Generates the Initial board state
        self.gameWon = self.STILLPLAYING
        self.maxDepth = 10

    def draw_board(self, width, height):
        for i in range(width):
            for j in range(height):
                if (j + i) % 2 == 0:
                    self.add_piece(gameBoard.BLACK_ICON, 1, i, j)
                else:
                    self.add_piece(gameBoard.WHITE_ICON, -1, i, j)

    def print_board(self):
        counter = 1
        print("Turn: " + str(self.turn - 1) + "\n")
        print("  _1__2__3__4__5__6__7__8_")
        s = ""
        for h in range(self.height):
            s = s + str(counter) + "| "
            for w in range(self.width):
                piece = self.total_pieces[h][w]
                if not piece == "-":
                    s = s + str(self.total_pieces[h][w].color) + "  "
                else:
                    s = s + "-- "
            s = s + " \n"
            counter += 1
        s = s + "\n" + "Last Move: " + self.last_move
        print(s)
        print("--------------------------")

    def toString(self):
        s = ""
        for h in range(self.height):
            for w in range(self.width):
                piece = self.total_pieces[h][w]
                if not piece == "-":
                    s = s + str(self.total_pieces[h][w].color) + "  "
                else:
                    s = s + "-- "
            s = s + "\n"
        s = s + "Turn:" + str(self.turn) + "\n" + "Last Move: " + self.last_move
        return s

    def is_legal_move(self, x1, y1, x2, y2):
        if (self.turn < 2):
            legal_moves = self.first_two_moves_picker(1)
            if [x1, y1] in legal_moves:
                return 1
            return 0

        difference_x = int(x2) - int(x1)
        difference_y = int(y2) - int(y1)
        pieces_jumped = []
        if (abs(difference_x) == 2 and abs(difference_y) == 0) or (abs(difference_x) == 0 and abs(difference_y) == 2):
            if self.total_pieces[x2][y2] == '-':
                if difference_y == 2:

                    if self.total_pieces[x2][y2 - 1] == "-" or self.total_pieces[x2][y2 - 1].color == \
                            self.total_pieces[x1][y1].color:
                        return 0
                    else:
                        pieces_jumped.append([x2, y2 - 1])
                if difference_y == -2:
                    if self.total_pieces[x2][y2 + 1] == "-" or self.total_pieces[x2][y2 + 1].color == \
                            self.total_pieces[x1][y1].color:
                        return 0
                    else:
                        pieces_jumped.append([x2, y2 + 1])
                if difference_x == 2:
                    if self.total_pieces[x2 - 1][y2] == "-" or self.total_pieces[x2 - 1][y2].color == \
                            self.total_pieces[x1][y1].color:
                        return 0
                    else:
                        pieces_jumped.append([x2 - 1, y2])
                if difference_x == -2:
                    if self.total_pieces[x2 + 1][y2] == "-" or self.total_pieces[x2 + 1][y2].color == \
                            self.total_pieces[x1][y1].color:
                        return 0
                    else:
                        pieces_jumped.append([x2 + 1, y2])
                return 1

        return 0

    # This is called to calculate pieces which need to be removed given a move
    def list_of_jumped_pieces(self, x1, y1, x2, y2):
        if (x2 == None or y2 == None):
            return []
        difference_x = int(x2) - int(x1)
        difference_y = int(y2) - int(y1)
        pieces_jumped = []

        if (abs(difference_x) == 2 and abs(difference_y) == 0) or (abs(difference_x) == 0 and abs(difference_y) == 2):
            if self.total_pieces[x2][y2] == '-':
                if difference_y == 2:
                    if self.total_pieces[x2][y2 - 1] != "-" and self.total_pieces[x2][y2 - 1].color != \
                            self.total_pieces[x1][y1].color:
                        pieces_jumped.append([x2, y2 - 1])

                if difference_y == -2:
                    if self.total_pieces[x2][y2 + 1] != "-" and self.total_pieces[x2][y2 + 1].color != \
                            self.total_pieces[x1][y1].color:
                        pieces_jumped.append([x2, y2 + 1])
                if difference_x == 2:
                    if self.total_pieces[x2 - 1][y2] != "-" and self.total_pieces[x2 - 1][y2].color != \
                            self.total_pieces[x1][y1].color:
                        pieces_jumped.append([x2 - 1, y2])
                if difference_x == -2:
                    if self.total_pieces[x2 + 1][y2] != "-" and self.total_pieces[x2 + 1][y2].color != \
                            self.total_pieces[x1][y1].color:
                        pieces_jumped.append([x2 + 1, y2])

        return pieces_jumped

    def remove_piece_from_board(self, x, y):
        piece = self.total_pieces[x][y]
        self.total_pieces[x][y] = "-"
        if piece.color == gameBoard.BLACK_ICON:
            del self.black_pieces[piece.piece_id]
        else:
            del self.white_pieces[piece.piece_id]

    # This method is used to derive a human player's requested destination
    def derive_coordinates(self, x1, y1, direction):
        if direction == 'u':
            return x1, y1 - 2
        if direction == 'd':
            return x1, y1 + 2
        if direction == 'l':
            return x1 - 2, y1
        if direction == 'r':
            return x1 + 2, y1
        if direction == 'p':
            return None, None

    def move_piece_human(self, piece_coordinates, direction):
        row, col = piece_coordinates
        x1 = int(col)
        y1 = int(row)
        x2 = None
        y2 = None
        direction_returned = self.derive_coordinates(x1, y1, direction)
        if not (direction_returned is None):
            x2 = direction_returned[0]
            y2 = direction_returned[1]
            if self.is_legal_move(x1, y1, x2, y2) == 0:
                print("Illegal move please try again (Middle)")
                return 0
        else:
            if self.is_legal_move(x1, y1, None, None) == 0:
                print("Illegal move please try again (Opening)")
                return 0

        if direction == 'p':
            self.update_game_piece_position(x1, y1, None, None)
        else:
            jumped = self.list_of_jumped_pieces(x1, y1, x2, y2)
            self.update_game_piece_position(x1, y1, x2, y2)
            for piece in jumped:
                self.remove_piece_from_board(piece[0], piece[1])
        self.turn = self.turn + 1
        return 1

    def expand_white_moves(self):
        for key, piece in self.white_pieces.items():
            for move in self.expand_moves_for_piece(piece):
                yield piece, move

    def print_w(self):
        g = self.expand_white_moves()
        for i in g:
            print(i)

    def expand_black_moves(self):
        for key, piece in self.black_pieces.items():
            for move in self.expand_moves_for_piece(piece):
                yield piece, move

    def expand_moves_for_piece(self, piece):
        return self.return_all_moves(piece)

    def first_two_moves_picker(self, legal_check):
        pieces = [self.total_pieces[0][0], self.total_pieces[self.width - 1][self.height - 1]
            , self.total_pieces[int(self.width / 2)][int(self.height / 2)],
                  self.total_pieces[int((self.width / 2) - 1)][int((self.height / 2) - 1)]]
        coordinates = [[0, 0], [self.width - 1, self.height - 1],
                       [int(self.width / 2), int(self.height / 2)],
                       [int((self.width / 2) - 1), int((self.height / 2) - 1)]]

        if self.turn == 0:
            return (random.choice(pieces), "--", self.turn + 1)

        else:
            white_has_to_pick_adjacent = None
            for it in coordinates:
                x = it[0]
                y = it[1]
                if self.total_pieces[x][y] == '-':
                    adj_x, adj_y = x, y
            if legal_check == 1:
                return self.generate_set_of_legal_moves_for_second_move(adj_x, adj_y)
            white_choice = random.choice(self.generate_set_of_legal_moves_for_second_move(adj_x, adj_y))
            x = white_choice[0]
            y = white_choice[1]

            return self.total_pieces[y][x], "--", self.turn + 1

    def generate_set_of_legal_moves_for_second_move(self, adjacent_x, adjacent_y):
        moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        legal_pieces_to_remove = []
        for move in moves:
            white_choice_x = move[0] + adjacent_x
            white_choice_y = move[1] + adjacent_y
            if not (self.width > white_choice_x > -1 and self.height > white_choice_y > -1):
                continue
            legal_pieces_to_remove.append([white_choice_x, white_choice_y])
        return legal_pieces_to_remove

    """
    The general movement options are the 4 cardinals:
    (-1,0)Left, (1,0)Right, (0,-1)Down, (0,1)Up. 

    The method below returns all possible legal moves from those above and 
    returns it will a turn counter to keep track of player switch. 

    """

    def iter_for_all_moves(self, piece):
        moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for move in moves:
            destination_x = move[0] + piece.x
            destination_y = move[1] + piece.y

            if not (self.width > destination_x > -1 and self.height > destination_y > -1):
                continue

            if self.total_pieces[destination_x][destination_y] == "-":
                continue
            else:
                if piece.color == self.total_pieces[destination_x][destination_y].color:
                    continue

                landing_x = move[0] + piece.x + move[0]
                landing_y = move[1] + piece.y + move[1]

                if not (self.width > landing_x > -1 and self.height > landing_y > -1):
                    continue
                if self.total_pieces[landing_x][landing_y] == "-":
                    yield (piece, [landing_x, landing_y], self.turn + 1)

    # Checks the amount of moves avaliable for each player and checks if either have no moves
    def player_has_no_moves(self, turn_color):
        for piece, move in self.expand_black_moves():
            print(piece.x, piece.y, move[0], move[1])
        for piece, move in self.expand_white_moves():
            print(piece.x, piece.y, move[0], move[1])
        if turn_color == gameBoard.BLACK_ICON:
            self.gameWon = gameBoard.WHITEWON
        else:
            self.gameWon = gameBoard.BLACKWON

    """
    NEW FUNCTIONS ADDED FOR MULTI JUMP PURPOSES
    """

    def computer_move(self, piece_coordinates, move_seq):
        x1, y1 = piece_coordinates
        x1 = int(x1)
        y1 = int(y1)

        if move_seq == "--":
            self.update_game_piece_position(x1, y1, None, None)
            self.turn = self.turn + 1
            return

        moves_to_execute = len(move_seq)
        index = 0
        last_move_string = "[" + str(x1 + 1) + "," + str(y1 + 1) + "]"
        while moves_to_execute > 0:
            x2 = int(move_seq[index][1:-4])
            y2 = int(move_seq[index][4:-1])
            last_move_string = last_move_string + " to " + "[" + str(x2 + 1) + "," + str(y2 + 1) + "]"
            self.execute_move(x1, y1, x2, y2)
            moves_to_execute -= 1
            index += 1
            x1 = x2
            y1 = y2
        self.last_move = last_move_string + " piece color: " + self.total_pieces[x1][y1].color
        # color = self.total_pieces[x1][y1].color
        # print("CURRENT TURN: " + str(self.turn))
        # print("CURRENT PIECE COLOR: " + str(color))
        self.turn = self.turn + 1

    def execute_move(self, x1, y1, x2, y2):
        pieces_to_remove_after_move = self.list_of_jumped_pieces(x1, y1, x2, y2)
        self.update_game_piece_position(x1, y1, x2, y2)
        for piece in pieces_to_remove_after_move:
            self.remove_piece_from_board(piece[0], piece[1])

    """
    Method to replace iter_for_all_moves_method
    """

    def return_all_moves(self, piece):
        row = piece.x
        col = piece.y
        original = "[" + str(row) + ", " + str(col) + "]"
        list_of_moves = self.generate_list_legal_moves(row, col, piece.color, None, 0)
        list_of_move_paths = self.legal_move_path_list(list_of_moves, original)
        for paths in list_of_move_paths:
            yield (piece, paths, self.turn + 1)

    """
    Method will take the list from the generate legal moves method, and generate paths for each of the possible moves
    """

    def legal_move_path_list(self, moves, original):
        # Keep track of a list of legal moves
        list_of_legal_moves = []
        index = 0
        for move in moves:
            # Get moveTo coordinate
            move_to = str((move[1])[8:])
            # Get parent move coordinate
            parent = str((move[2])[12:])
            # Now we have to determine if parent is equal to original coordinate
            if parent == original:
                # Means we can get to that move with just one move
                temp_list = [move_to]
                list_of_legal_moves.append(temp_list)
            else:
                backtracking_list = self.generate_path(moves, move[2], original, index)
                initial = [move_to]
                backtracking_list.extend(initial)
                list_of_legal_moves.append(backtracking_list)
            index += 1
        return list_of_legal_moves

    """
    Method used for generating a path based on a given starting coordinate and its list of moves
    """

    def generate_path(self, m, p, o, i):
        list_of_moves = []
        matching = []
        index = 0
        # Loop through to link moveTo at current index with a possible previous moveTo
        for move in m:
            move_to = (move[1])[8:]
            if p[12:] == move_to:
                matching.append(index)
            index += 1
        diff = i - matching[0]
        right_index = matching[0]
        counter = m[i][0]
        # Find which index is closest to the move we are concerned with
        for ind in matching:
            new_dff = i - ind
            # Based on how the list is sorted, the correct index cannot be greater than our current index
            if counter == 0:
                if new_dff > diff and ind < i:
                    diff = new_dff
                    right_index = ind
            else:
                if new_dff < diff and ind < i:
                    diff = new_dff
                    right_index = ind
        c_move = m[right_index]
        mi = (c_move[1])[8:]
        parent = c_move[2]
        if parent[12:] == o:
            list_of_moves.insert(0, mi)
        else:
            test = self.generate_path(m, parent, o, right_index)
            list_of_original = [mi]
            test.extend(list_of_original)
            list_of_moves.extend(test)
        return list_of_moves

    """
    Method for generating a list of all legal moves for a piece at a given row and column, r,c
    """

    def generate_list_legal_moves_straight(self, r, c, color, removed, count, direction):
        # Scan board for possible moves from the current x, y on the board
        moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        directions = ["N", "S", "E", "W"]
        legal_moves = []
        removed_list = []
        if not removed is None:
            removed_list.extend(removed)
        # print("I am generating legal moves for: " + str([r, c]))
        # print("I am working on this color: " + color)
        # print("The current removed_list is: " + str(removed_list))
        counter = 0
        for m in moves:
            current_direction = directions[counter]
            # If we are not going in the same direction automatically stop looking
            if direction is None or direction == current_direction:
                move_row = r + m[0]
                move_col = c + m[1]
                jumped = False
                # Check if the current move is valid to continue
                if self.is_within_bounds(move_row, move_col):
                    # print("Is within bounds: " + str([move_row, move_col]))
                    # If the space is not empty continue
                    # Now that we know it is in the board, loop to check if it has been jumped or not
                    current_piece = [move_row, move_col]
                    # print(current_piece)
                    for jumped_pieces in removed_list:
                        if current_piece == jumped_pieces:
                            jumped = True
                            # print("Piece has already been removed!")
                    if not (self.total_pieces[move_row][move_col] == '-') and not jumped:
                        # print("Move is not empty")
                        # If the new space is a piece with a different color continue
                        if not (self.total_pieces[move_row][move_col].color == color):
                            # print("Color of it is different as well")
                            # Check if the space beyond is empty
                            beyond_r = move_row + m[0]
                            beyond_c = move_col + m[1]
                            # Check if space past piece is valid as well
                            if self.is_within_bounds(beyond_r, beyond_c):
                                if self.total_pieces[beyond_r][beyond_c] == "-":
                                    # print("The piece we want to move to: " + str([beyond_r, beyond_c]))
                                    current = "MoveTo: " + str([beyond_r, beyond_c])
                                    parent = "ParentMove: " + str([r, c])
                                    removed_list.append([move_row, move_col])
                                    # print(removed_list)
                                    legal_moves.append([count, current, parent])
                                    # Store the list of possible multi jumps

                                    # print("The current count is at: " + str(count))
                                    count += 1
                                    legal_moves.extend(
                                        self.generate_list_legal_moves_straight(beyond_r, beyond_c, color, removed_list,
                                                                                count, current_direction))
                                    count = 0
                                    del removed_list[-1]
            counter += 1
        return legal_moves

    def generate_list_legal_moves(self, r, c, color, removed, count):
        # Scan board for possible moves from the current x, y on the board
        moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        legal_moves = []
        removed_list = []
        if not (removed is None):
            removed_list.extend(removed)
        counter = 0
        for m in moves:
            move_row = r + m[0]
            move_col = c + m[1]
            jumped = False
            # Check if the current move is valid to continue
            if self.is_within_bounds(move_row, move_col):
                # If the space is not empty continue
                # Now that we know it is in the board, loop to check if it has been jumped or not
                current_piece = [move_row, move_col]
                for jumped_pieces in removed_list:
                    if current_piece == jumped_pieces:
                        jumped = True
                if not (self.total_pieces[move_row][move_col] == '-') and not jumped:
                    # If the new space is a piece with a different color continue
                    if not (self.total_pieces[move_row][move_col].color == color):
                        # Check if the space beyond is empty
                        beyond_r = move_row + m[0]
                        beyond_c = move_col + m[1]
                        # Check if space past piece is valid as well
                        if self.is_within_bounds(beyond_r, beyond_c):
                            if self.total_pieces[beyond_r][beyond_c] == "-":
                                current = "MoveTo: " + str([beyond_r, beyond_c])
                                parent = "ParentMove: " + str([r, c])
                                removed_list.append([move_row, move_col])
                                legal_moves.append([count, current, parent])
                                count += 1
                                legal_moves.extend(
                                    self.generate_list_legal_moves(beyond_r, beyond_c, color, removed_list, count))
                                count = 0
                                del removed_list[-1]
            counter += 1
        return legal_moves

    """
    Method for checking of a given position is within the boundaries of the board
    """

    def is_within_bounds(self, x, y):
        if x > self.width - 1 or x < 0:
            return False
        if y > self.height - 1 or y < 0:
            return False
        return True

    """
    Method for printing the board object
    """

    def __str__(self):
        s = ""
        for h in range(self.height):
            for w in range(self.width):
                piece = self.total_pieces[h][w]
                if not piece == "-":
                    s = s + str(self.total_pieces[h][w].color) + "  "
                else:
                    s = s + "-- "
            s = s + "\n"
        s = s + "Last Move: " + self.last_move + "\n"
        return s

    def terminal_state(self, black_or_white):
        # Method will scan the board and see if we are in a terminal state
        # The idea is to check all the pieces for black and all the pieces for white
        # Return the color of the piece that can't move along with True if in terminal state
        list_of_black_moves = []
        list_of_white_moves = []

        # Check if black is in a terminal state
        if black_or_white == self.BLACK_ICON:
            for b, x in self.expand_black_moves():
                list_of_black_moves.append(x[1])
            if len(list_of_black_moves) == 0:
                return True
        # Check if white is in a terminal state
        elif black_or_white == self.WHITE_ICON:
            for b, x in self.expand_white_moves():
                list_of_white_moves.append(x[1])
            if len(list_of_white_moves) == 0:
                return True

        return False

    """
    All the code below this line is used for board evaluation and the different types of evals are inherent by its given name.

    """

    # This will be our Terminal check for Minimax

    def game_over(self):
        black_has_moves = 0
        white_has_moves = 0

        for piece, move in self.expand_black_moves():
            black_has_moves = 1
            break

        for piece, move in self.expand_white_moves():
            white_has_moves = 1
            break

        if black_has_moves == 0 and self.turn % 2 == 0:
            return -100000000000
        if white_has_moves == 0 and self.turn % 2 == 1:
            return 100000000000

        return 0

    def utility(self, eval):
        if eval == 1:
            return self.utility_number_of_pieces()
        if eval == 2:
            return self.utility_number_of_ally_moves()
        if eval == 3:
            return self.utility_number_of_enemy_moves()
        if eval == 4:
            return self.utility_number_of_ally_vs_enemy_moves()

    def utility_number_of_pieces(self):
        game_status = self.game_over()
        if game_status != 0:
            return game_status

        desirability = 0
        desirability -= len(self.black_pieces)
        desirability -= len(self.white_pieces)
        return desirability

    def utility_number_of_ally_moves(self):
        game_status = self.game_over()
        if game_status != 0:
            return game_status

        desirability = 0
        if self.turn % 2 == 0:
            desirability += len(list(self.expand_black_moves()))
        else:
            desirability -= len(list(self.expand_white_moves()))
        return desirability

    def utility_number_of_enemy_moves(self):
        game_status = self.game_over()
        if game_status != 0:
            return game_status

        desirability = 0
        if self.turn % 2 == 0:
            desirability -= len(list(self.expand_white_moves()))

        else:
            desirability += len(list(self.expand_black_moves()))
        return desirability

    def utility_number_of_ally_vs_enemy_moves(self):
        game_status = self.game_over()
        if game_status != 0:  # 0 means game still live
            return game_status

        return len(list(self.expand_black_moves())) - len(list(self.expand_white_moves()))

    def human_move(self, human_input):
        # Must contain to and smallest input is: 1,1 to 1,2 (one move) = 10 characters
        if not (" to " in human_input) or len(human_input) < 10:
            print("Wrong format, please try again")
            return 0
        # Check after splitting, should have 3 characters in each
        move_seq = human_input.split(" to ")
        length = len(move_seq)
        for i in range(length):
            if not (len(move_seq[i]) == 3):
                print("Wrong Format, please try again")
                return 0
        # At this point we can begin checking if moves are legal
        counter = 1
        piece_x = int(move_seq[0][:-2]) - 1
        piece_y = int(move_seq[0][2:]) - 1
        board_o = deepcopy(self)
        while counter < length:
            move_x = int(move_seq[counter][:-2]) - 1
            move_y = int(move_seq[counter][2:]) - 1
            # if the first one is legal then proceed, but we need a way to undo the damage
            if board_o.is_legal_move(piece_x, piece_y, move_x, move_y) == 0:
                print("Illegal move, please try again")
                return 0
            board_o.execute_move(piece_x, piece_y, move_x, move_y)
            board_o.increment_turn()
            piece_x = move_x
            piece_y = move_y
            counter += 1
        # At this point we know the moves are all legal so we execute them
        index = 1
        x1 = int(move_seq[0][:-2]) - 1
        y1 = int(move_seq[0][2:]) - 1
        last_move_string = "[" + str(x1 + 1) + "," + str(y1 + 1) + "]"
        while index < length:
            x2 = int(move_seq[index][:-2]) - 1
            y2 = int(move_seq[index][2:]) - 1
            last_move_string = last_move_string + " to " + "[" + str(x2 + 1) + "," + str(y2 + 1) + "]"
            self.execute_move(x1, y1, x2, y2)
            index += 1
            x1 = x2
            y1 = y2
        self.last_move = last_move_string + " piece color: " + self.total_pieces[x1][y1].color
        self.turn = self.turn + 1
        return 1

    def human_move_start(self, human_input):
        if not (len(human_input) == 3):
            print("Wrong format, please try again")
            return 0

        # This means we are black and get to remove a black piece
        if self.turn == 0:
            # Now check that it is one of the four possible moves to removed
            valid_moves = ["8,8", "1,1", "5,5", "4,4"]
            check = False
            for i in range(4):
                if human_input == valid_moves[i]:
                    check = True
                    break
            if not check:
                print("Illegal move, please try again")
                return 0
            else:
                x1 = int(human_input[:-2]) - 1
                y1 = int(human_input[2:]) - 1
                self.update_game_piece_position(x1, y1, None, None)
        # This means we are white and get to remove an adjacent piece
        if self.turn == 1:
            black_x = int(self.last_move[9:-18]) - 1
            black_y = int(self.last_move[11:-16]) - 1
            x1 = int(human_input[:-2]) - 1
            y1 = int(human_input[2:]) - 1
            valid_removes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            check2 = False
            for m in range(4):
                x, y = valid_removes[m]
                if x1 == black_x + x and y1 == black_y + y:
                    check2 = True
                    break

            if not check2:
                print("Illegal move, please try again")
                return 0
            else:
                self.update_game_piece_position(x1, y1, None, None)
        self.turn += 1
        return 1

    def increment_turn(self):
        self.turn += 1
