from typing import List, Tuple, Set

import numpy as np
from tqdm import tqdm

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions, DIRECTION_LABEL_TO_TUPLE


PERPENDICULARS = {"L": ["U", "D"], "R": ["U", "D"], "U": ["L", "R"], "D": ["L", "R"]}


class Day12(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def get_regions_and_perims(self, grid: np.array) -> List[Tuple]:
        regions = []

        while any([x != "." for x in np.unique(grid)]):
            possible_starts = [(int(x), int(y)) for x, y in zip(*np.where(grid != "."))]
            start = possible_starts[0]
            region = set([])
            nodes = [start]
            plant = grid[start]

            iters = 0
            while len(nodes) > 0:
                next_node = nodes.pop(0)
                region.add(next_node)
                for pos in get_adjacent_positions(next_node, grid.shape, include_diagonals=False):
                    if grid[pos] == plant and pos not in region and pos not in nodes:
                        nodes.append(pos)
                iters += 1

            perim_nodes = []
            for plot in list(region):
                for pos in get_adjacent_positions(plot, grid.shape, include_diagonals=False):
                    if grid[pos] != plant:
                        perim_nodes.append(pos)
            regions.append((region, perim_nodes))

            for plot in list(region):
                grid[plot] = "."

        return regions

    def part1(self, data: List[str]) -> int:
        grid = NumpyArrayParser(data).parse()
        grid = np.pad(grid, 1, "constant", constant_values=".")

        regions = self.get_regions_and_perims(grid)
        region_prices = 0
        for region, perim in regions:
            region_prices += len(region) * len(perim)

        return region_prices

    def get_tuple_in_direction(self, node: Tuple[int], direction: Tuple[int]) -> Tuple[int]:
        return tuple([p + d for p, d in zip(node, direction)])

    def get_fence_from_candidate(
        self, perim_node: Tuple[int], grid: np.array, region_plant: str, perims_probed: Set
    ) -> List:
        fences = []
        for direction_label, direction_tuple in DIRECTION_LABEL_TO_TUPLE.items():
            fence_candidate = (perim_node, direction_tuple)
            if fence_candidate in perims_probed:
                continue
            region_probe = tuple([p + d for p, d in zip(*fence_candidate)])

            try:
                if grid[region_probe] != region_plant:
                    continue
            except IndexError:
                continue

            # Now we know that the opposite side of the fence to this perim
            # node is a target plant, so we can try to construct a fence
            new_fence = [fence_candidate]
            for perp_dir_label in PERPENDICULARS[direction_label]:
                perp_dir_tuple = DIRECTION_LABEL_TO_TUPLE[perp_dir_label]
                nodes = [self.get_tuple_in_direction(fence_candidate[0], perp_dir_tuple)]
                while len(nodes) > 0:
                    new_check_node = nodes.pop()
                    new_node_probe = self.get_tuple_in_direction(new_check_node, direction_tuple)
                    if grid[new_node_probe] == region_plant:
                        new_fence.append((new_check_node, direction_tuple))
                        nodes.append(self.get_tuple_in_direction(new_check_node, perp_dir_tuple))
            fences.append(new_fence)
            perims_probed.update(new_fence)

        return fences

    def part2(self, data: List[str]) -> int:
        grid = NumpyArrayParser(data).parse()
        grid = np.pad(grid, 1, "constant", constant_values=".")
        grid_full = np.copy(grid)

        regions = self.get_regions_and_perims(grid)
        grid = grid_full
        region_prices = 0
        for region, perim in regions:
            all_fences = []
            perims_probed = set([])
            unique_perims = list(set(perim))
            region_plant = grid[list(region)[0]]
            for unique_perim in unique_perims:
                # We will create fence candidates
                all_fences.append(
                    self.get_fence_from_candidate(unique_perim, grid, region_plant, perims_probed)
                )
            reduced_fences = set([])
            reduced_fences = set([])
            for fence_group in all_fences:
                for fence in fence_group:
                    if len(fence) > 0:
                        reduced_fence = "|".join([str(x[0]) for x in sorted(fence)])
                        reduced_fences.add(reduced_fence)
            curr_region_price = len(reduced_fences) * len(region)
            print(
                f"REGION {region_plant} EQUATION IS {len(region)} * {len(reduced_fences)} = {curr_region_price}"
            )
            region_prices += curr_region_price

        # 678332 TOO LOW
        return region_prices


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day12(day, use_sample, run_each)
    solver.solve()
