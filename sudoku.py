from typing import List, Tuple, Optional, Set
from os import system
from time import sleep


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    with open(filename) as f:
        content = f.read()
    digits = [c for c in content if c in '123456789.']
    # noinspection PyTypeChecker
    grid = group(digits, 9)
    return grid


def group(values: List[int], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix = []
    k = 0
    avalues = values.copy()
    for _ in avalues:
        while k < n:
            matrix.append(avalues[:n])
            k += 1
            avalues = avalues[n:]
    return matrix


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    for i in range(9):
        if i == pos[0]:
            return grid[i]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [row[pos[1]] for row in grid]


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    y, x = pos
    block_y = y // 3
    block_x = x // 3
    for row in grid[block_y * 3:block_y * 3 + 3]:
        for cell in row[block_x * 3:block_x * 3 + 3]:
            block.append(cell)
    return block


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '.':
                return y, x


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество всех возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzles/puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    values = []
    taken_val = set(get_row(grid, pos) + get_col(grid, pos) + get_block(grid, pos))
    for val in '123456789':
        if val not in taken_val:
            values.append(val)
    return set(values)


def print_grid(grid: List[List[str]]) -> None:
    if grid:
        for row in grid:
            print(' '.join(row))


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid
    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
    ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
    ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
    ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
    ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
    ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
    ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
    ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
    ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    y, x = pos
    possible_values = find_possible_values(grid, pos)
    for val in possible_values:
        grid[y][x] = val
        # system('cls')
        # print_grid(grid)
        # print(val, pos)
        # sleep(0.2)
        solution = solve(grid)
        if solution and is_solved(solution):
            return solution
        grid[y][x] = '.'


def is_solved(grid: List[List[str]]) -> bool:
    for row in grid:
        if '.' in row:
            return False
    for y in range(9):
        for x in range(9):
            if sum(map(int, get_row(grid, (y, x)))) + \
                sum(map(int, get_col(grid, (y, x)))) + \
                    sum(map(int, get_block(grid, (y, x)))) == 135:
                return True


if __name__ == '__main__':
    sudoku_grid = read_sudoku('puzzle1.txt')
    print_grid(solve(sudoku_grid))
