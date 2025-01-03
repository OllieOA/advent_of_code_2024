# Using a numpy grid, here are some useful common functions

from typing import List, Tuple, Iterable, Dict
import numpy as np


DIRECTION_LABEL_TO_TUPLE = {"L": (0, -1), "U": (-1, 0), "R": (0, 1), "D": (1, 0)}
DIRECTION_TUPLE_TO_LABEL = {v: k for k, v in DIRECTION_LABEL_TO_TUPLE.items()}


class GridVisualiser:
    def __init__(self, grid: Iterable, spec: Dict = dict()):
        self.grid = grid
        self.spec = spec

    def visualise_grid(self):
        display_grid = "\n"
        for row in self.grid:
            for col in row:
                display_grid += self.spec.get(col, col)
            display_grid += "\n"
        print(display_grid)


def get_tuple_in_direction(node: Tuple[int], direction: Tuple[int]) -> Tuple[int]:
    return tuple([p + d for p, d in zip(node, direction)])


def get_adjacent_positions(
    pos: Tuple[int],
    arr_shape: Tuple[int],
    include_diagonals: bool = True,
    direction: Tuple = None,
    step_size: int = 1,
) -> List[Tuple]:
    """Get all adjacent positions ()

    Args:
        pos (Tuple[int]): start pos
        arr_shape (Tuple[int]): shape of the array
        include_diagonals (bool): include diagonals from pos

    Returns:
        List[Tuple]: _description_
    """
    if direction:
        positions = [(pos[0] + direction[0], pos[1] + direction[1])]
    else:
        positions = [
            (pos[0] + step_size, pos[1]),
            (pos[0] - step_size, pos[1]),
            (pos[0], pos[1] + step_size),
            (pos[0], pos[1] - step_size),
        ]

    if include_diagonals and not direction:
        diag_positions = [
            (pos[0] - step_size, pos[1] - step_size),
            (pos[0] - step_size, pos[1] + step_size),
            (pos[0] + step_size, pos[1] - step_size),
            (pos[0] + step_size, pos[1] + step_size),
        ]
        positions.extend(diag_positions)

    if include_diagonals and direction:
        raise ValueError("Cannot consider both diagonals and a given direction")

    filtered_positions = []
    for pos in positions:
        x, y = pos
        if x < 0 or x >= arr_shape[0] or y < 0 or y >= arr_shape[1]:
            # print(f"FILTERING OUT ({x}, {y})")
            continue
        filtered_positions.append(pos)
    return filtered_positions


def get_manhattan_dist(point1: Tuple[int], point2: Tuple[int]) -> int:
    return sum([abs(p1 - p2) for p1, p2 in zip(point1, point2)])


def get_euler_dist(point1: Tuple[int], point2: Tuple[int]) -> float:
    return np.sqrt(sum([(p1 + p2) ** 2 for p1, p2 in zip(point1, point2)]))
