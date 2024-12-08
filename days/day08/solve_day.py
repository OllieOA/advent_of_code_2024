from itertools import combinations
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day08(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def check_if_point_in_grid(self, point: Tuple[int], grid_shape: Tuple[int]) -> bool:
        in_grid = True
        for px, bx in zip(point, grid_shape):
            in_grid = in_grid and not (px < 0 or px >= bx)

        return in_grid

    def part1(self, data: List[str]) -> int:
        """The strategy here is to get all combinations of antennas, and then
        use the difference to "step" past each one to find the antinode."""
        grid = NumpyArrayParser(data).parse()

        signals = [str(x) for x in np.unique(grid)]
        signals.remove(".")

        antinodes = set([])

        for antenna_type in signals:
            antennas_of_type = [(int(x), int(y)) for x, y in zip(*np.where(grid == antenna_type))]
            for a1, a2 in combinations(antennas_of_type, 2):
                diff = (a1[0] - a2[0], a1[1] - a2[1])
                antinode_loc1 = (a1[0] + diff[0], a1[1] + diff[1])
                antinode_loc2 = (a2[0] - diff[0], a2[1] - diff[1])

                if self.check_if_point_in_grid(antinode_loc1, grid.shape):
                    antinodes.add(antinode_loc1)
                if self.check_if_point_in_grid(antinode_loc2, grid.shape):
                    antinodes.add(antinode_loc2)

        return len(antinodes)

    def get_all_antinodes(
        self, point_1: Tuple[int], point_2: Tuple[int], grid_shape: Tuple[int]
    ) -> List[Tuple[int]]:
        diff = (point_1[0] - point_2[0], point_1[1] - point_2[1])

        in_grid = True
        p1_antinodes = [point_1]
        while in_grid:
            next_antinode = (p1_antinodes[-1][0] + diff[0], p1_antinodes[-1][1] + diff[1])
            in_grid = self.check_if_point_in_grid(next_antinode, grid_shape)
            if in_grid:
                p1_antinodes.append(next_antinode)

        in_grid = True
        p2_antinodes = [point_2]
        while in_grid:
            next_antinode = (p2_antinodes[-1][0] - diff[0], p2_antinodes[-1][1] - diff[1])
            in_grid = self.check_if_point_in_grid(next_antinode, grid_shape)
            if in_grid:
                p2_antinodes.append(next_antinode)

        return p1_antinodes + p2_antinodes

    def part2(self, data: List[str]) -> int:
        """Similarly, we need to do the same as part one, but instead of just
        one step, we will continue stepping in one direction until we hit the
        end of the grid, and then "turn around", go back to the start, and
        step back along it"""
        grid = NumpyArrayParser(data).parse()

        signals = [str(x) for x in np.unique(grid)]
        signals.remove(".")

        antinodes = set([])
        for antenna_type in signals:
            antennas_of_type = [(int(x), int(y)) for x, y in zip(*np.where(grid == antenna_type))]
            for a1, a2 in combinations(antennas_of_type, 2):
                all_antinodes = self.get_all_antinodes(a1, a2, grid.shape)
                antinodes.update(all_antinodes)

        return len(antinodes)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day08(day, use_sample, run_each)
    solver.solve()
