from typing import List

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions


class Day20(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day
        if use_sample:
            self.min_cheat_to_count = 12
        else:
            self.min_cheat_to_count = 100

    def part1(self, data: List[str]) -> int:
        self.grid = NumpyArrayParser(data).parse()

        start_pos = np.where(self.grid == "S")
        start_pos = (int(start_pos[0][0]), int(start_pos[1][0]))

        end_pos = np.where(self.grid == "E")
        end_pos = (int(end_pos[0][0]), int(end_pos[1][0]))

        dist_from_start = {}
        path = [start_pos]
        self.steps = []
        visited = set([])

        curr_cost = 0
        while len(path) > 0:
            curr_pos = path.pop(0)
            dist_from_start[curr_pos] = curr_cost
            curr_cost = len(dist_from_start)

            visited.add(curr_pos)
            self.steps.append(curr_pos)
            if curr_pos == end_pos:
                break

            for adj_pos in get_adjacent_positions(
                curr_pos, self.grid.shape, include_diagonals=False
            ):
                if adj_pos in visited:
                    continue
                if self.grid[adj_pos] == "#":
                    continue
                path.append(adj_pos)

        dist_from_end = {}
        for pos, dist in dist_from_start.items():
            dist_from_end[pos] = dist_from_start[end_pos] - dist

        # Now, we walk through the path and see if there is a possible link

        cheats = {}
        total_len = len(self.steps)
        for step in self.steps:
            for overwall_pos in get_adjacent_positions(
                step, self.grid.shape, include_diagonals=False, step_size=2
            ):
                if overwall_pos in dist_from_end:
                    saved_picoseconds = (
                        (dist_from_end[overwall_pos] + dist_from_start[step]) - 1
                    ) - total_len
                    if saved_picoseconds < self.min_cheat_to_count:  # Ignore
                        continue
                    if saved_picoseconds not in cheats:
                        cheats[saved_picoseconds] = []
                    cheats[saved_picoseconds].append(step)

        return sum([len(v) for v in cheats.values()])

    def part2(self, data: List[str]) -> None:
        self.part1(data)  # Need the grid and stuff

        all_cheats = {}
        # This will be a dictionary with the key being the start point, and
        # a list of tuples which are the cheats defined as the position reached
        # and the picoseconds to get there


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day20(day, use_sample, run_each)
    solver.solve()
