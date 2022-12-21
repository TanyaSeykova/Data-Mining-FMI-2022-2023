board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

MAX_SCORE = 10
MIN_SCORE = -10

empty_cell = '-'
computer_symbol = 'O'
player_symbol = 'X'

LEN_BOARD = 3
INFINITY = float('inf')
invalid_position = -1

def evaluate_board(depth):
    global board
    for row in range(LEN_BOARD):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == computer_symbol:
                return MAX_SCORE - depth
            elif board[row][0] == player_symbol:
                return MIN_SCORE + depth
    
    # check cols for victory
    for col in range(LEN_BOARD):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == computer_symbol:
                return MAX_SCORE - depth
            if board[0][col] == player_symbol:
                return MIN_SCORE + depth

    # check main diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == computer_symbol:
            return MAX_SCORE - depth
        if board[0][0] == player_symbol:
            return MIN_SCORE + depth

    # check secondary diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == computer_symbol:
            return MAX_SCORE - depth
        if board[0][2] == player_symbol:
            return MIN_SCORE + depth
    
    return 0

def print_board():
    global board
    for line in board:
        print("\n-------------")
        for char in line:
            print(f"| {char} ", end = '')
        print(f"|", end = '')
    print("\n-------------")

def has_free_moves():
    global board
    for row in range(LEN_BOARD):
        for col in range(LEN_BOARD):
            if board[row][col] == empty_cell:
                return True
    return False

def maximizer(alpha, beta, depth):
    global board
    current_score = evaluate_board(depth)

    if current_score != 0:
        return current_score
    
    if not has_free_moves():
        return 0

    best_score = -INFINITY

    for row in range(LEN_BOARD):
        for col in range(LEN_BOARD):
            if board[row][col] == empty_cell:
                board[row][col] = computer_symbol
                
                best_score = max(best_score, minimizer(alpha, beta, depth + 1))

                board[row][col] = empty_cell

                if best_score >= beta:
                    return best_score
                
                alpha = max(alpha, best_score)
    return best_score
    
def minimizer(alpha, beta, depth):
    global board
    current_score = evaluate_board(depth)

    if current_score != 0:
        return current_score
    
    if not has_free_moves():
        return 0

    best_score = INFINITY

    for row in range(LEN_BOARD):
        for col in range(LEN_BOARD):
            if board[row][col] == empty_cell:
                board[row][col] = player_symbol

                best_score = min(best_score, maximizer(alpha, beta, depth + 1))

                board[row][col] = empty_cell

                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)
    return best_score

def find_best_move_for_computer():
    global board
    best_value = -INFINITY
    best_next_turn = invalid_position, invalid_position

    for row in range(LEN_BOARD):
        for col in range(LEN_BOARD):
            if board[row][col] == empty_cell:
                board[row][col] = computer_symbol

                current_move_value = minimizer(-INFINITY, INFINITY, 0)

                board[row][col] = empty_cell

                if (current_move_value > best_value):
                    best_next_turn = row, col
                    best_value = current_move_value
    return best_next_turn

def has_winner():
    if evaluate_board(0) != 0:
        return True
    return False

def make_move(row, col, is_player_turn):
    global board
    if board[row ][col] != empty_cell:
        print("This is not an empty cell. Try again, please.")
        return False
    if not 0 <= row <= 2 or not 0 <= col <= 2:
        print("This is not a valid input. Rows and columns should be between 1 and 3")
        return False
     
    if is_player_turn:
        board[row][col] = player_symbol
    else:
        board[row][col] = computer_symbol
    
    print_board()

    if has_winner():
        if is_player_turn:
            print("Good job, buddy! You have won!")
        else:
            print("Aww, you lost, but you did great. Better luck next time ;)")
    elif not has_free_moves():
        print("You are tied!")
    return True

def initialize_game():
    print("Choose 1 to start first, and 0 to start second 0/1")
    choice = input()
    if choice != '0' and choice != '1':
        print("Invalid input. Try again")
        return False
    
    if choice == '0':
        global player_symbol
        player_symbol = 'O'
        global computer_symbol 
        computer_symbol = 'X'    
    
    return True
  

def main():
    print("Choose 0 to start first, and 1 to start second 0/1")
    choice = input()
    if choice != '0' and choice != '1':
        print("Invalid input. Try again")
        return False
    
    is_player_turn = True
    if choice == '1': # is computer turn
        global player_symbol
        player_symbol = 'O'
        global computer_symbol 
        computer_symbol = 'X'
        is_player_turn = False
    
    while has_free_moves() and not has_winner():
        if is_player_turn:
            trigger = True
            while trigger:
                row, col = input("Enter row and column: ").split()
                row = int(row)
                col = int(col)
                if make_move(row - 1, col - 1, is_player_turn):
                    trigger = False
            is_player_turn = not is_player_turn
            continue

        best_turn = find_best_move_for_computer()
        make_move(best_turn[0], best_turn[1], is_player_turn)
        is_player_turn = not is_player_turn

if __name__ == "__main__":
    main()
