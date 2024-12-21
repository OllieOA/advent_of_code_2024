from typing import List

import numpy as np

from solver import Solver
from utils.grid_utils import get_adjacent_positions


class Day21(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.numeric_keypad = np.array(
            [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]]
        )

        self.directional_keypad = np.array(
            [
                ["", "^", "A"],
                ["<", "v", ">"],
            ]
        )

    def find_sequence(self, sequence: str, target_keypad: np.array) -> str:
        curr_pos = np.where(target_keypad == "A")
        curr_pos = (int(curr_pos[0][0]), int(curr_pos[1][0]))

        needed_seq = ""
        for target_button in sequence:
            target_pos = np.where(target_keypad == target_button)
            target_pos = (int(target_pos[0][0]), int(target_pos[1][0]))
            req_vector = tuple([p1 - p2 for p1, p2 in zip(target_pos, curr_pos)])

            j_step_dir = -1 if req_vector[0] < 0 else 1
            i_step_dir = -1 if req_vector[1] < 0 else 1
            for j in range(0, req_vector[0] + (j_step_dir // abs(j_step_dir)), j_step_dir):
                if j == 0:
                    continue
                needed_seq += "^" if j < 0 else "v"
            for i in range(0, req_vector[1] + (i_step_dir // abs(i_step_dir)), i_step_dir):
                if i == 0:
                    continue
                needed_seq += "<" if i < 0 else ">"
            needed_seq += "A"
            curr_pos = target_pos
        return needed_seq

    def get_complexity(self, numeric_sequence: str, needed_sequence: str) -> int:
        numeric = int("".join([x for x in numeric_sequence if x.isnumeric()]))
        return len(needed_sequence) * numeric

    def part1(self, data: List[str]) -> int:
        complexities = []
        for numeric_sequence in data:
            needed_seq = self.find_sequence(numeric_sequence, self.numeric_keypad)
            for _ in range(2):
                needed_seq = self.find_sequence(needed_seq, self.directional_keypad)

            complexity = self.get_complexity(numeric_sequence, needed_seq)
            print(
                f"SEQUENCE {numeric_sequence} NEEDS {needed_seq} OF LENGTH {len(needed_seq)} COMPLEXITY {complexity}"
            )
            complexities.append(complexity)

        return sum(complexities)

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day21(day, use_sample, run_each)
    solver.solve()
