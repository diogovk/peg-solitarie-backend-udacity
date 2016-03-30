
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
    """
    origin_peg_x = letter_to_index(move[0][0])
    # we subtract 1 since externally indexes start at 1 instead of 0
    origin_peg_y = int(move[0][1])-1
    if not in_bounds(origin_peg_x, origin_peg_y):
        raise InvalidMoveExpection("The origin peg is out of bounds")
    direction = move[1].lower()
    if direction not in VALID_DIRECTIONS:
        raise ValueError("The direction should be one of the following "
                         "options: 'up','down','left','right'")
    dest_peg = peg_destination(origin_peg_x, origin_peg_y, direction[0])
    if not in_bounds(dest_peg[0], dest_peg[1]):
        raise InvalidMoveExpection(
                "The destination of the move is out of bounds")


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
