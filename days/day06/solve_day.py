from copy import deepcopy
from typing import List, Tuple, Dict

import numpy as np
from tqdm import tqdm

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day06(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.next_dir_lookup = {
            (0, 1): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
        }

        self.curr_dir_code_lookup = {
            (-1, 0): "U",
            (1, 0): "D",
            (0, 1): "R",
            (0, -1): "L",
        }

        self.curr_dir_reverse_lookup = {v: k for k, v in self.curr_dir_code_lookup.items()}

    def traverse_map(self, grid: np.array) -> Tuple[np.array, List, bool]:
        """The strategy is to "cast a ray" (in reality this iterates over each
        element which could surely be optimised with a slice) until it hits
        either a 1 or a 2 (2 is a padded edge on the grid)

        Any stepped on cell gets set to a value of 3, and then we just count
        those at the end (we do not turn a 2 into a 3, otherwise we would have
        to subtract 1)
        """
        curr_dir = (-1, 0)

        start_x, start_y = np.where(grid == 9)
        curr_pos = (int(start_x[0]), int(start_y[0]))

        solved = False
        infinite = False

        path = []

        while not solved:
            # Cast a ray out until a non-zero value is hit
            ray = [curr_pos]
            while grid[ray[-1]] != 1 or grid[ray[-1]] != 2:
                if grid[ray[-1]] == 2:
                    solved = True
                    break
                elif grid[ray[-1]] == 1:
                    break
                else:
                    ray.append((ray[-1][0] + curr_dir[0], ray[-1][1] + curr_dir[1]))

            for ray_pos in ray[:-1]:
                grid[ray_pos] = 3
                path_code = (
                    f"{",".join([str(x) for x in ray_pos])}_{self.curr_dir_code_lookup[curr_dir]}"
                )
                if path_code in path:
                    infinite = True
                    return grid, path, infinite
                path.append(path_code)

            curr_dir = self.next_dir_lookup[curr_dir]
            curr_pos = ray[-2]

        return grid, path, infinite

    def part1(self, data: List[str]) -> int:
        grid_raw = NumpyArrayParser(data).parse()

        replace_map = {".": 0, "#": 1, "^": 9}
        grid = deepcopy(grid_raw)
        for key, val in replace_map.items():
            grid[grid_raw == key] = val
        grid = grid.astype(int)
        grid = np.pad(grid, 1, constant_values=2)

        grid, _, _ = self.traverse_map(grid)

        _, counts = np.unique(grid, return_counts=True)

        return counts[3]

    def part2(self, data: List[str]) -> None:
        """Naive solution here - trace a path and then check every path with a
        single modification in front of the path. This can be optimised with
        sub paths and a better traversal function"""
        grid_raw = NumpyArrayParser(data).parse()

        replace_map = {".": 0, "#": 1, "^": 9}
        grid = deepcopy(grid_raw)
        for key, val in replace_map.items():
            grid[grid_raw == key] = val

        grid = grid.astype(int)
        grid = np.pad(grid, 1, constant_values=2)

        start_x, start_y = np.where(grid == 9)
        start_pos = (int(start_x[0]), int(start_y[0]))

        clear_grid = deepcopy(grid)
        _, path, _ = self.traverse_map(grid)

        # Format of the path:
        # ['7,5_U', '6,5_U', '5,5_U...

        infinite_attempts = set([])
        for step in tqdm(path):
            check_grid = np.copy(clear_grid)
            modify_pos = [int(x) for x in step.split("_")[0].split(",")]

            if ",".join([str(x) for x in modify_pos]) in infinite_attempts:
                continue

            if all([x == y for x, y in zip(modify_pos, start_pos)]):
                continue  # This is the start pos

            check_grid[modify_pos[0], modify_pos[1]] = 1

            _, _, infinite = self.traverse_map(check_grid)
            if infinite:
                infinite_attempts.add(",".join([str(x) for x in modify_pos]))

        return len(infinite_attempts)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day06(day, use_sample, run_each)
    solver.solve()
