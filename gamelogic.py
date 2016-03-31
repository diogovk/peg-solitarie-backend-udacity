from rpc_messages import GameMessage

BOARD_SIZE = 7
VALID_DIRECTIONS = ['u', 'd', 'l', 'r', 'up', 'down', 'left', 'right']

INITIAL_BOARD = ['  ***  ',
                 '  ***  ',
                 '*******',
                 '***o***',
                 '*******',
                 '  ***  ',
                 '  ***  ']


class InvalidMoveExpection(Exception):
    pass


def move(current_state, move):
    """
    Moves a peg if a valid move is passed, returning the new game state.
    Receives a Game and in case of success changes its fields with the new state.
    This method doesn't commit, so you must .put() manually if you want to save the new state.
    Returns a reference to the game object.
    """
    cur_board = current_state.board[:]
    # origin validations
    origin_x = letter_to_index(move[0][0])
    # we subtract 1 since externally indexes start at 1 instead of 0
    origin_y = int(move[0][1])-1
    if not in_bounds(origin_x, origin_y):
        raise InvalidMoveExpection("The origin peg is out of bounds")
    origin_tile = cur_board[origin_y][origin_x]
    if origin_tile == ' ':
        raise InvalidMoveExpection(
                "The origin of the move is an unusable space( ). "
                "In a valid move, the origin should be a peg(*).")
    if origin_tile == 'o':
        raise InvalidMoveExpection(
                "The origin of the move is a hole(o). "
                "In a valid move, the origin should be a peg(*).")
    # direction validations
    direction = move[1].lower()
    if direction not in VALID_DIRECTIONS:
        raise ValueError("The direction should be one of the following "
                         "options: 'up','down','left','right'")
    dest = peg_destination(origin_x, origin_y, direction[0])
    if not in_bounds(dest[0], dest[1]):
        raise InvalidMoveExpection(
                "The destination of the move is out of bounds")
    dest_tile = cur_board[dest[1]][dest[0]]
    if dest_tile == ' ':
        raise InvalidMoveExpection(
                "The destination of the move is an unusable space( ). "
                "In a valid move, the destination should be a hole(o)")
    if dest_tile == '*':
        raise InvalidMoveExpection(
                "The destination of the move is a peg(*). "
                "In a valid move, the destination should be a hole(o)")
    # Jump validations
    jump = between(origin_x, origin_y, dest[0], dest[1])
    jump_tile = cur_board[jump[1]][jump[0]]
    if jump_tile != "*":
        raise InvalidMoveExpection(
                'The "jump" position does not have a peg(*). '
                'In a valid move the "jump" must have a peg(*).')
    # update new board
    cur_board[origin_y] = replace_char(cur_board[origin_y], "o", origin_x)
    cur_board[dest[1]] = replace_char(cur_board[dest[1]], "*", dest[0])
    cur_board[jump[1]] = replace_char(cur_board[jump[1]], "o", jump[0])
    current_state.board = cur_board
    return current_state

def letter_to_index(letter):
    """ Changes 'a'..'g' into '0..6' """
    letter = letter.lower()
    # 97 is 'a' in ascii table
    return ord(letter)-97


def in_bounds(position_x, position_y):
    """ Check if point is within borders of the BOARD """
    return (position_x >= 0 and position_x < BOARD_SIZE and
            position_y >= 0 and position_y < BOARD_SIZE)


def peg_destination(origin_x, origin_y, direction):
    """
    Calculate the destination position when jumping from a point in a
    certain direction
    """
    dict_move = {"u": (0, -2),  # up
                 "d": (0, +2),  # down
                 "l": (-2, 0),  # left
                 "r": (+2, 0)}  # right
    move = dict_move[direction]
    return (origin_x+move[0], origin_y+move[1])


def between(origin_x, origin_y, dest_x, dest_y):
    """ Returns the point between two points """
    return ((origin_x+dest_x)/2, (origin_y+dest_y)/2)


def replace_char(string, char, position):
    return string[:position] + char + string[position+1:]
