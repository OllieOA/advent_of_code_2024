from collections import Counter
from typing import List

from solver import Solver


class Day01(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def build_lists(self, data: List[str]) -> None:
        left_list = []
        right_list = []
        for line in data:
            left_num, right_num = [int(x) for x in line.split(" ") if x.isnumeric()]
            left_list.append(left_num)
            right_list.append(right_num)

        self.left_list = left_list
        self.right_list = right_list

    def part1(self, data: List[str]) -> None:
        self.build_lists(data)
        left_list = sorted(self.left_list)
        right_list = sorted(self.right_list)

        res = 0
        for l, r in zip(left_list, right_list):
            res += abs(l - r)
        return res

    def part2(self, data: List[str]) -> None:
        self.build_lists(data)

        right_list_stats = Counter(self.right_list)

        res = 0
        for num in self.left_list:
            res += num * right_list_stats[num]
        return res


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day01(day, use_sample, run_each)
    solver.solve()
