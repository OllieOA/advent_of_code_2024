from collections import Counter
from copy import deepcopy
from typing import List, Dict, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions


class Day10(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def flood_fill(self, grid: np.array, start_point: Tuple[int], uphill: bool) -> Dict:
        visited = set([])
        path = [start_point]
        endpoints_accessible = set([])
        while len(path) > 0:
            curr_node = path.pop(0)
            target_val = grid[curr_node] + 1 if uphill else grid[curr_node] - 1
            visited.add(curr_node)
            for point in get_adjacent_positions(curr_node, grid.shape, include_diagonals=False):
                if point not in visited:
                    if grid[point] == target_val and uphill:
                        if target_val < 9:
                            path.append(point)
                        else:
                            endpoints_accessible.add(point)
                    elif grid[point] == target_val and not uphill:
                        if target_val > 0:
                            path.append(point)
                        else:
                            endpoints_accessible.add(point)
        return {"endpoints_accessible": endpoints_accessible, "visited": visited}

    def part1(self, data: List[str]) -> int:
        """Here will we do a flood fill (aka breadth first search but don't
        stop when a solution is found) out from each trailhead and count the
        number of accessible peaks"""
        grid = NumpyArrayParser(data).parse()
        grid = np.astype(grid, int)

        peaks = [(int(x), int(y)) for x, y in zip(*np.where(grid == 9))]
        trailheads = {}
        for peak in peaks:
            path_info = self.flood_fill(grid, peak, uphill=False)

            trailheads_accessible = path_info["endpoints_accessible"]
            for trailhead in list(trailheads_accessible):
                if trailhead not in trailheads:
                    trailheads[trailhead] = 0
                trailheads[trailhead] += 1

        return sum(trailheads.values())

    def part2(self, data: List[str]) -> None:
        """We will generate the path info from all peaks downhill and
        trailheads uphill, then combine the visited paths sets in a union to
        find all nodes that connect them"""

        grid = NumpyArrayParser(data).parse()
        grid = np.astype(grid, int)

        trailheads = [(int(x), int(y)) for x, y in zip(*np.where(grid == 0))]
        peaks = [(int(x), int(y)) for x, y in zip(*np.where(grid == 9))]

        downhill_data = {}
        uphill_data = {}

        for peak in peaks:
            downhill_data[peak] = self.flood_fill(grid, peak, uphill=False)

        for trailhead in trailheads:
            uphill_data[trailhead] = self.flood_fill(grid, trailhead, uphill=True)

        """From here, we can iterate over each trailhead and do a very simple
        BFS and only care about number of options in each step, because we know 
        what grid points are not included in the path so
        we don't need to worry about """

        ratings = {}
        for trailhead in uphill_data.keys():
            ratings[trailhead] = 0
            uphill_visited = uphill_data[trailhead]["visited"]
            for accessible_peak in uphill_data[trailhead]["endpoints_accessible"]:
                downhill_visited = downhill_data[accessible_peak]["visited"]
                common_visited = downhill_visited.intersection(uphill_visited)
                common_visited.add(accessible_peak)

                paths = [[trailhead]]
                while all([len(p) < 10 for p in paths]):
                    new_paths = []
                    while len(paths) > 0:
                        curr_path = paths.pop(0)
                        target_val = grid[curr_path[-1]] + 1
                        if target_val == 10:
                            raise ValueError("SHOULDN'T GET HERE")
                        any_identified = False
                        for pos in get_adjacent_positions(
                            curr_path[-1], grid.shape, include_diagonals=False
                        ):
                            if pos not in common_visited:
                                continue
                            if grid[pos] == target_val:
                                any_identified = True
                                new_sub_path = deepcopy(curr_path)
                                new_sub_path.append(pos)
                                new_paths.append(new_sub_path)
                        if not any_identified:
                            raise ValueError(f"CAN'T FIND NEXT STEP IN PATH {curr_path}")

                    paths = new_paths

                tuple_paths = [tuple(p) for p in paths]
                # for p in list(tuple_paths):
                #     print(p)
                # raise
                ratings[trailhead] += len(set(tuple_paths))

        return sum(ratings.values())


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day10(day, use_sample, run_each)
    solver.solve()
