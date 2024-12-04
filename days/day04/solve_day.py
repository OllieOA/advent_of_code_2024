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
        """The strategy here is to find all X's which will be the start of a
        potential word. Then, we simply need to check if the characters in that
        direction form the target XMAS word. This requires us to build out the
        needed indices.
        """
        grid = NumpyArrayParser(data).parse()
        starters = []

        # Find all X's which will start a word
        xs, ys = np.where(grid == "X")
        starters = [(int(x), int(y)) for x, y in zip(xs, ys)]

        num_words = 0

        for starter in starters:
            adjacent_candidates = get_adjacent_positions(
                starter, grid.shape, include_diagonals=True, step_size=3
            )

            # Find 4 characters away in all directions

            for candidate in adjacent_candidates:
                slices = {}
                for ax, idx in zip(["x", "y"], range(2)):
                    if starter[idx] == candidate[idx]:
                        # Here, we need a list of the same number
                        slices[ax] = 4 * [starter[idx]]
                    else:
                        # Here, we need a diagonal list (note the +step_dir given ranges are end-exclusive)
                        step_dir = 1 if starter[idx] < candidate[idx] else -1
                        slices[ax] = list(
                            range(
                                starter[idx],
                                candidate[idx] + step_dir,
                                step_dir,
                            )
                        )

                # Construct based on the slices definition we made above
                candidate_word = "".join(
                    [str(grid[slices["x"][n], slices["y"][n]]) for n in range(4)]
                )
                if candidate_word == "XMAS":
                    num_words += 1

        return num_words

    def part2(self, data: List[str]) -> int:
        """Given we now need to consider shape, we can use some constraints to
        shrink our search space. Firstly, we now use the A as a starter point
        and generate the diagonals immediately adjacent.

        Our logic check is simple. Necessarily:
        - We need 2 S and 2 M, and
        - We need one character to share at least a horizonal or vertical.

        The reason there is because if they did NOT share, we would have

        M S
         A
        S M

        MAM and SAS.
        """
        grid = NumpyArrayParser(data).parse()
        starters = []

        xs, ys = np.where(grid == "A")
        starters = [(int(x), int(y)) for x, y in zip(xs, ys)]

        dirs = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        num_xmases = 0
        for starter in starters:
            adjacent_candidates = []
            for each_dir in dirs:
                candidate = get_adjacent_positions(
                    starter, grid.shape, include_diagonals=False, direction=each_dir
                )
                if len(candidate) == 0:
                    break
                adjacent_candidates.append(candidate[0])

            # Now we have 4 candidates - if 2 are M and 2 are S, AND the Ms share a dimension, we have an X-MAS
            tracker = {"M": [], "S": []}
            for candidate in adjacent_candidates:
                if grid[candidate] not in tracker.keys():
                    # Not M or S
                    break
                tracker[grid[candidate]].append(candidate)

            if len(tracker["M"]) != 2 or len(tracker["S"]) != 2:
                # Characters are not balanced
                continue

            if (
                tracker["M"][0][0] != tracker["M"][1][0]
                and tracker["M"][0][1] != tracker["M"][1][1]
            ):
                # Characters do not share a dimension (i.e. diagonally opposite - MAM and SAS)
                continue

            num_xmases += 1

        return num_xmases


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day04(day, use_sample, run_each)
    solver.solve()
