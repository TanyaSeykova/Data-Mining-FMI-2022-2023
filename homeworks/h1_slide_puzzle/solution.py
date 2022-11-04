from cmath import inf
import datetime
import math
import timeit

correct_positions = {}
manhattan_for_tile = {}
tiles = []

def read_input():

    lines = []
    num_tiles = int(input())
    pos_empty = int(input())

    num_lines = math.sqrt(num_tiles + 1)
    num_lines = int(num_lines)

    for index in range(num_lines):
        lines.append(input())
        tiles.append(lines[index].split())

    return num_tiles, num_lines, pos_empty


def fill_correct_pos(num_tiles, num_lines, pos_empty):
    begin = 1
    if pos_empty == -1:
        correct_positions[0] = (num_lines - 1, num_lines - 1)
    else:
        correct_positions[0] = ((int)((pos_empty - 1) / num_lines), (pos_empty - 1) % num_lines)

    tile = 1
    for tile in range(1, num_tiles + 1):
        if pos_empty == -1:
            correct_positions[tile] = ((int)((tile - 1) / num_lines), (tile - 1) % num_lines)
        else:
            if tile < pos_empty:
                correct_positions[tile] = ((int)((tile - 1) / num_lines), (tile - 1) % num_lines)
            else:
                correct_positions[tile] = ((int)((tile) / num_lines), (tile) % num_lines)
        
def to_list_tiles():
    tiles_list = []
    for row in tiles:
        for tile in row:
            if tile == '0':
                continue
            tiles_list.append(tile)

    return tiles_list


def check_if_solvable():
    list_tiles = to_list_tiles()
    inv_count = 0
    for i in range(len(list_tiles)):
        for j in range(i, len(list_tiles)):
            if(list_tiles[j] < list_tiles[i]):
                inv_count += 1
    
    if inv_count % 2 == 0:
        return True
    return False

def evaluate_manhattan_for_tile(tile, current_pos):
    return abs(correct_positions[tile][0] - current_pos[0]) + abs(correct_positions[tile][1] - current_pos[1])


def manhattan():
    result = 0
    len_ = len(tiles)
    for row in range(len_):
        for col in range(len_):
            tile = int(tiles[row][col])
            if  tile == 0:
                continue
            dist = evaluate_manhattan_for_tile(tile, (row, col))
            manhattan_for_tile[tile] = dist
            result += dist
    return result


def move_tile(pos_empty, pos_tile):
    tiles[pos_empty[0]][pos_empty[1]], tiles[pos_tile[0]][pos_tile[1]] = tiles[pos_tile[0]][pos_tile[1]], tiles[pos_empty[0]][pos_empty[1]]

def is_goal():
    return manhattan() == 0

def get_pos_zero():
    for row in range(len(tiles)):
        for col in range (len(tiles)):
            if tiles[row][col] == '0':
                return (row, col)

def move_up():
    pos_zero = get_pos_zero()
    if pos_zero[0] < len(tiles) - 1:
        move_tile(pos_zero, (pos_zero[0] + 1, pos_zero[1]))
        return True
    else:
        return False

def move_down():
    pos_zero = get_pos_zero()
    if pos_zero[0] > 0:
        move_tile(pos_zero, (pos_zero[0] - 1, pos_zero[1]))
        return True
    else:
        return False
def move_left():
    pos_zero = get_pos_zero()
    if pos_zero[1] < len(tiles) - 1:
        move_tile(pos_zero, (pos_zero[0], pos_zero[1] + 1))
        return True
    else:
        return False
def move_right():
    pos_zero = get_pos_zero()
    if pos_zero[1] > 0:
        move_tile(pos_zero, (pos_zero[0], pos_zero[1] - 1))
        return True
    else:
        return False


FOUND = -3
INFINITY = float(inf)
path = ["start"]
def search(current_cost, threshold):
    f = current_cost + manhattan()
    if f > threshold:
        return f
    if is_goal():
        return FOUND
    minimum = INFINITY
    last_move = path[-1]
    if last_move != "up" and move_down():
        path.append("down")
        t = search(current_cost + 1, threshold)
        if t == FOUND:
            return FOUND
        if t < minimum:
            minimum = t
        path.pop()
        move_up()

    if last_move != "down" and move_up():
        path.append("up")
        t = search(current_cost + 1, threshold)
        if t == FOUND:
            return FOUND
        if t < minimum:
            minimum = t
        path.pop()
        move_down()

    if last_move != "left" and move_right():
        path.append("right")
        t = search(current_cost + 1, threshold)
        if t == FOUND:
            return FOUND
        if t < minimum:
            minimum = t
        path.pop()
        move_left()

    if last_move != "right" and move_left():
        path.append("left")
        t = search(current_cost + 1, threshold)
        if t == FOUND:
            return FOUND
        if t < minimum:
            minimum = t
        path.pop()
        move_right()
    return minimum
    


def ida_star():
    threshold = manhattan()

    while True:
        t = search(0, threshold)
        if t == FOUND:
            return path
        threshold = t


def handle_result():
    
    start_time = datetime.datetime.now()
    ida_star()
    end_time = datetime.datetime.now()
    path.pop(0)
    print(len(path))
    for move in path:
        print(move)

    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()

    print('Execution time:', execution_time)


def main():
    num_tiles, num_lines, pos_empty = read_input()

    if not check_if_solvable():
        print("The puzzle is unsolvable!")
        return
    
    fill_correct_pos(num_tiles, num_lines, pos_empty)
    handle_result()

if __name__ == "__main__":
    main()