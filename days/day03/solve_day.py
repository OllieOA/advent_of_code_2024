import re
from typing import List

from solver import Solver


class Day03(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.mul_pattern = r"mul\((\d+),(\d+)\)"

    def part1(self, data: List[str]) -> int:
        """Today's strategy is simple - we will use regex to capture the
        relevant chunks, then form the operations into numeric form.
        """
        full_str = "".join([line for line in data])

        all_matches = re.findall(self.mul_pattern, full_str)

        curr_total = 0
        for match in all_matches:
            curr_total += int(match[0]) * int(match[1])

        return curr_total

    def part2(self, data: List[str]) -> None:
        """This is a bit of a mix between regex and a state machine. We find
        the indexes of all "switches", then we start extracting sub strings.

        Then, we can use the same regex pattern from part 1 to check the
        numeric value.
        """
        full_str = "".join([line for line in data])

        all_dos = [x.start() for x in re.finditer(r"do\(\)", full_str)]
        all_donts = [x.start() for x in re.finditer(r"don't\(\)", full_str)]

        # Collect all relevant substrings based on a flipped state
        # Could not figure out the regex pattern for this one, so just went
        # back to implementing it per the instructions

        enabled_substrs = []
        curr_str = ""
        enabled = True
        for idx in range(len(full_str)):
            if enabled:
                curr_str += full_str[idx]
                if idx in all_donts:
                    enabled_substrs.append(curr_str)
                    curr_str = ""
                    enabled = False
            else:
                enabled = idx in all_dos

        if enabled:
            enabled_substrs.append(curr_str)

        curr_total = 0
        for enabled_str in enabled_substrs:

            all_matches = re.findall(self.mul_pattern, enabled_str)
            for match in all_matches:
                curr_total += int(match[0]) * int(match[1])

        return curr_total


#  95846796
# 163401319
# 163401319 too high


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day03(day, use_sample, run_each)
    solver.solve()
