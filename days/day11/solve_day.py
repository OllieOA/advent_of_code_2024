from typing import List, Dict

from solver import Solver


class Day11(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.stone_rules = {}

    def get_new_stone(self, n) -> List[int]:
        if n in self.stone_rules:
            return self.stone_rules[n]

        if n == 0:
            self.stone_rules[n] = [1]
            return [1]

        str_n = str(n)
        if len(str_n) % 2 == 0:
            m1 = int(str_n[: (len(str_n) // 2)])
            m2 = int(str_n[(len(str_n) // 2) :])
            self.stone_rules[n] = [m1, m2]
            return [m1, m2]

        self.stone_rules[n] = [n * 2024]
        return [n * 2024]

    def blink(self, b, stone_counts: Dict) -> int:
        for _ in range(b):
            new_stone_counts = {}
            for stone, count in stone_counts.items():
                new_stones = self.get_new_stone(stone)
                for new_stone in new_stones:
                    if new_stone not in new_stone_counts:
                        new_stone_counts[new_stone] = 0
                    new_stone_counts[new_stone] += count
            stone_counts = new_stone_counts
        return sum(stone_counts.values())

    def part1(self, data: List[str]) -> int:
        """We've seen this trick before - check the wording of the question:
        the order does not matter, no matter how many times it is emphasised.
        All we need to do is keep a tally of the counts, and how the stones
        transform (just to cache it; makes it slightly faster)"""
        initial_stones = [int(x) for x in data[0].split(" ")]
        stone_counts = {}
        for stone in initial_stones:
            if stone not in stone_counts:
                stone_counts[stone] = 0
            stone_counts[stone] += 1

        num_stones = self.blink(25, stone_counts)

        return num_stones

    def part2(self, data: List[str]) -> None:
        """Here, we just run it again! Easy - if we were tracking this as a
        list, it would not be possible to keep everything in memory (List of
        len 250,783,680,217,283)"""
        initial_stones = [int(x) for x in data[0].split(" ")]
        stone_counts = {}
        for stone in initial_stones:
            if stone not in stone_counts:
                stone_counts[stone] = 0
            stone_counts[stone] += 1

        num_stones = self.blink(75, stone_counts)

        return num_stones


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day11(day, use_sample, run_each)
    solver.solve()
