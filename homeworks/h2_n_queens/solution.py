import datetime
import random

NUM_RESTARTS = 3
queens = []
queens_per_row = []
queens_main_d = []
queens_second_d = []
num_current_conflicts = 0

def read_input():

    global N 
    N = int(input())
    if N <= 0 or (N == 2 or N == 3):
        print("There is no solution!")
        return False
    return True

def fill_empty_lists():
    global queens
    queens = [0] * N # queen[col_index] = row of queen
    global queens_per_row
    queens_per_row = [0] * N
    global queens_main_d
    queens_main_d = [0] * (2 * N - 1)
    global queens_second_d
    queens_second_d = [0] * (2 * N - 1)

    # number of moves for restart
    global MOVES_FOR_RESTART
    MOVES_FOR_RESTART = 2 * N

    global num_current_conflicts
    num_current_conflicts = 0

def get_main_diagonal(col, row):
    return row - col + N - 1

def get_second_diagonal(col, row):
    return col + row


def calculate_conflics(col, row, no_queen):
    # if there is no queen currently in the cell, we shouldn't decrease
    if no_queen:
        return queens_per_row[row] + queens_main_d[get_main_diagonal(col, row)] + queens_second_d[get_second_diagonal(col, row)]
    return queens_per_row[row] - 1 + queens_main_d[get_main_diagonal(col, row)] - 1 + queens_second_d[get_second_diagonal(col, row)] - 1

# move to position (col, row)
def increment_conflicts(col, row):
    global num_current_conflicts
    num_current_conflicts += queens_per_row[row] + queens_main_d[get_main_diagonal(col, row)] + queens_second_d[get_second_diagonal(col, row)]
    
    queens_per_row[row] += 1
    queens_main_d[get_main_diagonal(col, row)]  += 1
    queens_second_d[get_second_diagonal(col, row)]  += 1

# move away from position (col, row)
def decrement_conflicts(col, row):
    global num_current_conflicts
    
    queens_per_row[row] -= 1
    queens_main_d[get_main_diagonal(col, row)]  -= 1
    queens_second_d[get_second_diagonal(col, row)]  -= 1
    
    num_current_conflicts = num_current_conflicts - queens_per_row[row] - queens_main_d[get_main_diagonal(col, row)] - queens_second_d[get_second_diagonal(col, row)]


def initialize_board():
    first_queen_row = random.randrange(0, N) # choose row for queen in first column
    queens[0] = first_queen_row
    
    increment_conflicts(0, first_queen_row)
    
    for col in range(1, N):
        conflicts_per_row = []
        for row in range(N):
            conflicts_per_row.append(calculate_conflics(col, row, True))
        min_row = conflicts_per_row.index(min(conflicts_per_row))
        queens[col] = min_row
        increment_conflicts(col, min_row)


def has_conflicts():
    return num_current_conflicts != 0

def get_col_with_queen_with_max_conflicts(last_move_col):
    conflits = []
    for col, row in enumerate(queens):
        conflits.append(calculate_conflics(col, row, False))

    max_conflict_indexes = []
    max_conflics = max(conflits)

    # There are no conflicts
    if max_conflics == 0:
        return -1

    # get all max conflict columns
    for ind, num_conflicts in enumerate(conflits):
        if num_conflicts == max_conflics:
            max_conflict_indexes.append(ind)
    
    # do not move last moved queen
    if len(max_conflict_indexes) > 1:
        if last_move_col in max_conflict_indexes:
            max_conflict_indexes.remove(last_move_col)
    return random.choice(max_conflict_indexes)

def get_row_with_min_conflicts(col):
    conflicts_per_row = [0] * N
    for row in range(N):
        if queens[col] == row:
            conflicts_per_row[row] += calculate_conflics(col, row, False)
        else:
            conflicts_per_row[row] += calculate_conflics(col, row, True)
    
    
    min_conflicts_indexes = []
    min_conflicts = min(conflicts_per_row)

    for ind, num_conflicts in enumerate(conflicts_per_row):
        if num_conflicts == min_conflicts:
            min_conflicts_indexes.append(ind)

    return random.choice(min_conflicts_indexes)

def solve():
    initialize_board()
    num_moves = 0
    last_move_col = -1
    if not has_conflicts():
        # Already solved
        return True
    while num_moves <= MOVES_FOR_RESTART:
        col = get_col_with_queen_with_max_conflicts(last_move_col)
        
        # There are no conflicts
        if col == -1:
            return True

        current_row = queens[col]

        row = get_row_with_min_conflicts(col)
        queens[col] = row

        decrement_conflicts(col, current_row)
        increment_conflicts(col, row)

        num_moves += 1
        last_move_col = col

    if has_conflicts():
        # restart
        fill_empty_lists()
        return False
    else:
        return True

def print_desk():
    if N > 25:
        return
    
    output_rev = []
    for ind in queens:
        curr_col = []
        curr_col.extend(['_'] * ind)
        curr_col.append('*')
        curr_col.extend(['_'] * (N - 1 - ind))
        output_rev.append(curr_col)

    # transpose result
    output = [[output_rev[j][i] for j in range(len(output_rev))] for i in range(len(output_rev[0]))]

    to_print = '\n'.join([''.join(['{:2}'.format(item) for item in row]) for row in output])
    print(to_print)
        

def start_from_restart():
    while(True):
        if solve():
            break

def main():
    if not read_input():
        return
    fill_empty_lists()
    
    start_time = datetime.datetime.now()
    start_from_restart()
    end_time = datetime.datetime.now()

    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()
    print_desk()
    print('Execution time:', execution_time)
    


if __name__ == "__main__":
    main()