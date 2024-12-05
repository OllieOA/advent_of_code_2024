from functools import cmp_to_key
from typing import List

from utils.parsers import NewLineListParser
from solver import Solver


class Day05(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def _create_problem_data(self, data: List[str]) -> None:
        ordering, updates = NewLineListParser(data).parse()
        ordering_dict = {}
        for ordering_info in ordering:
            x, y = ordering_info.split("|")
            if int(x) not in ordering_dict:
                ordering_dict[int(x)] = []
            ordering_dict[int(x)].append(int(y))

        self.ordering_dict = ordering_dict
        self.updates = updates

    def _check_if_correct(self, update: str) -> bool:
        """The approach is to step through - if there are no relation in the
        rules between the number and each number linked by a rule (in the
        dictionary), we can safely ignore. Otherwise, we just need to check if
        the index of the target later number is less than the current number we
        are on."""

        update_valid = True
        check_list = [int(x) for x in update.split(",")]

        for idx, num in enumerate(check_list):
            target_later_nums = self.ordering_dict.get(num, [])

            # If the number does not have a linked target ordering, there
            # will not be a violated rule
            if len(target_later_nums) == 0:
                continue

            for target_later_num in target_later_nums:
                # If the target number is not in the checklist, there will not
                # be a violated rule
                if not target_later_num in check_list:
                    continue

                # Order incorrect
                if check_list.index(target_later_num) <= idx:
                    update_valid = False
                    break

        return update_valid, check_list[len(check_list) // 2]

    def part1(self, data: List[str]) -> int:
        self._create_problem_data(data)

        middle_numbers = []

        for update in self.updates:
            update_valid, mid_number = self._check_if_correct(update)
            if update_valid:
                middle_numbers.append(mid_number)

        return sum(middle_numbers)

    def _custom_sort(self, a, b):
        """Custom comparer for the `sort()` function. Negative if a needs to
        be earler (as b is in the ordering_dict)
        """
        must_be_later = self.ordering_dict.get(a, [])

        cmp = -1 if b in must_be_later else 1

        return cmp

    def part2(self, data: List[str]) -> int:
        self._create_problem_data(data)

        middle_numbers = []

        for update in self.updates:
            update_valid, _ = self._check_if_correct(update)
            if update_valid:
                continue

            # We have something incorrectly ordered
            check_list = [int(x) for x in update.split(",")]
            check_list.sort(key=cmp_to_key(self._custom_sort))
            middle_numbers.append(check_list[len(check_list) // 2])

        return sum(middle_numbers)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day05(day, use_sample, run_each)
    solver.solve()
