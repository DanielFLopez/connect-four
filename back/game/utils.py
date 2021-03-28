from game.models import Game

MIN_VALUE, MAX_VALUE = 0, 6
CONNECT_VALUES = 4


def process_game(column=None, row=None, user=None, game=None):
    column, row, game = int(column), int(row), int(game)
    game = Game.objects.get(pk=game)
    result = validate_move(column, row, game)
    if result['is_valid']:
        matrix = game.matrix
        matrix[row][column] = game.get_user_code(user)
        game.set_matrix(matrix)
        if validate_win(column, row, matrix):
            game.set_winner(user)
            return {'is_winner': True, 'message': f"{user} WINS!!!", 'matrix_value': matrix}
        elif game.check_tied_game():
            return {'is_winner': True, 'message': "TIED GAME :/", 'matrix_value': matrix}
        game.change_turn()
    return {'turn': game.get_user_by_turn(), 'matrix_value': game.matrix, 'is_winner': False}


def validate_move(column=None, row=None, game=None):
    valid_initial_columns = [MIN_VALUE, MAX_VALUE]
    matrix = game.matrix
    prev_value = matrix[row][column]
    if prev_value == 0 and MIN_VALUE <= column <= MAX_VALUE:
        if column in valid_initial_columns:
            return {'is_valid': True}
        elif MIN_VALUE < column < MAX_VALUE and bool(matrix[row][column - 1] or matrix[row][column + 1]):
            return {'is_valid': True}
    return {'message': 'Invalid move', 'is_valid': False}


def validate_win(column, row, matrix):
    if validate_horizonal_vector(matrix, column, row):
        return True
    elif validate_vertical_vector(matrix, column, row):
        return True
    elif validate_diagonal_up_vector(matrix, column, row):
        return True
    elif validate_diagonal_down_vector(matrix, column, row):
        return True
    return False


def validate_horizonal_vector(matrix, column, row):
    min_value = max(column - (CONNECT_VALUES - 1), MIN_VALUE)
    max_value = min(column + (CONNECT_VALUES - 1), MAX_VALUE)
    consecutive_values = 0
    value = matrix[row][column]
    for c in range(min_value, max_value + 1):
        if matrix[row][c] == value:
            consecutive_values += 1
        else:
            consecutive_values = 0

        if consecutive_values >= CONNECT_VALUES:
            return True
        elif max_value - c < CONNECT_VALUES and consecutive_values == 0:
            return False


def validate_vertical_vector(matrix, column, row):
    min_value = max(row - (CONNECT_VALUES - 1), MIN_VALUE)
    max_value = min(row + (CONNECT_VALUES - 1), MAX_VALUE)
    consecutive_values = 0
    value = matrix[row][column]
    for r in range(min_value, max_value + 1):

        if matrix[r][column] == value:
            consecutive_values += 1
        else:
            consecutive_values = 0

        if consecutive_values >= CONNECT_VALUES:
            return True
        elif max_value - r < CONNECT_VALUES and consecutive_values == 0:
            return False


def validate_diagonal_up_vector(matrix, column, row):
    distance_back = get_back_increasing_diagonal_distance(row, column)
    distance_front = get_front_increasing_diagonal_distance(row, column)

    size = distance_back + distance_front + 1

    if size < CONNECT_VALUES:
        return False

    max_value_row = row + distance_back
    max_value_column = column - distance_back

    consecutive_values = 0
    value = matrix[row][column]

    for v in range(size):
        if matrix[max_value_row - v][max_value_column + v] == value:
            consecutive_values += 1
        else:
            consecutive_values = 0

        if consecutive_values >= CONNECT_VALUES:
            return True
        elif size - v < CONNECT_VALUES and consecutive_values == 0:
            return False


def validate_diagonal_down_vector(matrix, column, row):
    distance_back = get_back_decreasing_diagonal_distance(row, column)
    distance_front = get_front_decreasing_diagonal_distance(row, column)

    size = distance_back + distance_front + 1

    if size < CONNECT_VALUES:
        return False

    min_value_row = row - distance_back
    min_value_column = column - distance_back

    consecutive_values = 0
    value = matrix[row][column]

    for v in range(size):
        if matrix[min_value_row + v][min_value_column + v] == value:
            consecutive_values += 1
        else:
            consecutive_values = 0

        if consecutive_values >= CONNECT_VALUES:
            return True
        elif size - v < CONNECT_VALUES and consecutive_values == 0:
            return False


def get_back_decreasing_diagonal_distance(row, column):
    if row < (CONNECT_VALUES - 1) or column < (CONNECT_VALUES - 1):
        distance_back = min(row, column)
    else:
        distance_back = (CONNECT_VALUES - 1)
    return distance_back


def get_front_decreasing_diagonal_distance(row, column):
    if row + (CONNECT_VALUES - 1) > MAX_VALUE or column + (CONNECT_VALUES - 1) > MAX_VALUE:
        distance_front = min(MAX_VALUE - row, MAX_VALUE - column)
    else:
        distance_front = (CONNECT_VALUES - 1)
    return distance_front


def get_back_increasing_diagonal_distance(row, column):
    if column < (CONNECT_VALUES - 1) or row + (CONNECT_VALUES - 1) > MAX_VALUE:
        distance_back = min(column, MAX_VALUE - row)
    else:
        distance_back = CONNECT_VALUES - 1
    return distance_back


def get_front_increasing_diagonal_distance(row, column):
    if row > (CONNECT_VALUES - 1) > column:
        distance_front = CONNECT_VALUES - 1
    else:
        distance_front = min(row, MAX_VALUE - column)
    return distance_front
