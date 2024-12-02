import concurrent.futures as cf

from typing import List

from solver import Solver


class Day02(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def _check_safe(self, nums: List[int]) -> bool:
        if nums[0] == nums[1]:
            return False
        increasing = (nums[1] - nums[0]) > 0
        diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
        abs_diffs = [abs(x) for x in diffs]

        if (increasing and any([x < 0 for x in diffs])) or (
            not increasing and any([x > 0 for x in diffs])
        ):
            return False

        if any([x < 1 or x > 3 for x in abs_diffs]):
            return False

        return True

    def part1(self, data: List[str]) -> None:
        all_res = []
        for line in data:
            nums = [int(x) for x in line.split(" ")]
            all_res.append(self._check_safe(nums))
        return all_res.count(True)

    def part2(self, data: List[str]) -> None:
        all_res = []
        for line in data:
            nums = [int(x) for x in line.split(" ")]
            if self._check_safe(nums):
                all_res.append(True)
            else:
                # Check all possibilities of removed levels
                all_lines = []
                for idx in range(len(nums)):
                    all_lines.append([x for i, x in enumerate(nums) if i != idx])
                all_res.append(any([self._check_safe(x) for x in all_lines]))

        return all_res.count(True)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day02(day, use_sample, run_each)
    solver.solve()
