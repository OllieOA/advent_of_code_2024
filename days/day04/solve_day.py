from copy import deepcopy
from typing import List

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions
from utils.grid_utils import GridVisualiser


class Day04(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> int:
        grid = NumpyArrayParser(data).parse()
        starters = []

        xs, ys = np.where(grid == "X")
        starters = [(int(x), int(y)) for x, y in zip(xs, ys)]

        num_words = 0

        correct_words = []

        for starter in starters:
            adjacent_candidates = get_adjacent_positions(
                starter, grid.shape, include_diagonals=True, step_size=3
            )

            for candidate in adjacent_candidates:
                slices = {}
                for ax, idx in zip(["x", "y"], range(2)):
                    if starter[idx] == candidate[idx]:
                        slices[ax] = 4 * [starter[idx]]
                    else:
                        step_dir = 1 if starter[idx] < candidate[idx] else -1
                        slices[ax] = list(
                            range(
                                starter[idx],
                                candidate[idx] + step_dir,
                                step_dir,
                            )
                        )

                print(f"starter: {starter}, candidate: {candidate}")
                print(slices)

                candidate_word = "".join(
                    [str(grid[slices["x"][n], slices["y"][n]]) for n in range(4)]
                )
                print(f"candidate word: {candidate_word}")
                print("\n\n")
                if candidate_word == "XMAS":
                    num_words += 1
                    correct_words.append(slices)

        all_positions = []
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                all_positions.append((i, j))
        for slice in correct_words:
            for x, y in zip(slice["x"], slice["y"]):
                try:
                    all_positions.remove((x, y))
                except ValueError:
                    continue

        grid_copy = deepcopy(grid)

        for position in all_positions:
            grid_copy[position] = "."

        for idx in range(grid_copy.shape[0]):
            print("".join(list(grid_copy[idx, :])))

        return num_words

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day04(day, use_sample, run_each)
    solver.solve()
