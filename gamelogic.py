
BOARD_SIZE=7
VALID_DIRECTIONS=['u', 'd', 'l', 'r', 'up','down','left','right']

class InvalidMoveExpection(Exception):
    pass

def move(current_state, move):
    """
    Moves a peg if a valid move is passed, returning the new game state.
    Throws InvalidMoveExpection otherwize
    """
    origin_peg_x=letter_to_index(move[0][0])
    # we subtract 1 since externally indexes start at 1 instead of 0
    origin_peg_y=int(move[0][1])-1
    if not in_bounds(origin_peg_x, origin_peg_y):
        raise InvalidMoveExpection("The origin peg is out of bounds")
    direction=move[1].lower()
    if direction not in VALID_DIRECTIONS:
        raise ValueError("The direction should be"
                "one of the following options: 'up','down','left','right'")

def letter_to_index(letter):
    ''' Changes 'a'..'g' into '0..6' '''
    letter = letter.lower()
    # 97 is 'a' in ascii table
    return ord(letter)-97

def in_bounds(position_x, position_y):
    return (position_x >= 0 and position_x < BOARD_SIZE and
            position_y >= 0 and position_y < BOARD_SIZE)

