from typing import List, Dict

from tqdm import tqdm

from solver import Solver
from utils.parsers import NewLineListParser


class Day19(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def count_possible_arrangements(self, towel_request: str, memory: Dict = {}) -> int:
        if towel_request == "":  # Used for when we are at the end of the string - no more combos
            return 1
        if towel_request in memory:  # If we have seen this substr before, return it
            return memory[towel_request]

        # Pre-filter the towels to reduce the search space
        colors_in_spec = set(towel_request)
        valid_towels = []
        for t in self.available_towels:
            if len(self.unique_colors[t].difference(colors_in_spec)) > 0:
                # Here, there are more colours available in the sub-towel than possible in the spec
                continue
            if t not in towel_request:
                # Here, the sequence doesn't appear anywhere
                continue
            valid_towels.append(t)

        valid_portions = 0
        for t in valid_towels:
            if towel_request.startswith(t):
                leftover = towel_request[len(t) :]
                valid_portions += self.count_possible_arrangements(leftover, memory)

        memory[towel_request] = valid_portions
        return valid_portions

    def part1(self, data: List[str]) -> int:
        towel_spec, towels_requested = NewLineListParser(data).parse()

        self.available_towels = towel_spec[0].split(", ")
        self.unique_colors = {t: set(t) for t in self.available_towels}

        num_possible = 0
        for towel_request in tqdm(towels_requested):
            num_possible += 1 if self.count_possible_arrangements(towel_request) > 0 else 0

        return num_possible

    def part2(self, data: List[str]) -> int:
        towel_spec, towels_requested = NewLineListParser(data).parse()

        self.available_towels = towel_spec[0].split(", ")
        self.unique_colors = {t: set(t) for t in self.available_towels}

        combos = 0
        for towel_request in towels_requested:
            combos += self.count_possible_arrangements(towel_request)

        return combos


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day19(day, use_sample, run_each)
    solver.solve()
