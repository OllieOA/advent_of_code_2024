from typing import List

from solver import Solver
from utils.parsers import NewLineListParser


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.a_cost = 3
        self.b_cost = 1

    def calculate_cost(self, case: List[str], prize_offset: int = 0) -> int:
        for spec in case:
            target = spec.split(":")[0]
            spec_details = spec.split(":")[1]
            x_val = int("".join([x for x in spec_details.split(",")[0] if x.isnumeric()]))
            y_val = int("".join([x for x in spec_details.split(",")[1] if x.isnumeric()]))
            match target:
                case "Button A":
                    ax = x_val
                    ay = y_val
                case "Button B":
                    bx = x_val
                    by = y_val
                case "Prize":
                    px = x_val + prize_offset
                    py = y_val + prize_offset
                case _:
                    raise ValueError("Shouldn't get here!")

        m = (px * ay - py * ax) / (bx * ay - by * ax)
        n = (py - m * by) / ay

        if m % 1 != 0 or n % 1 != 0:
            return 0

        return n * self.a_cost + m * self.b_cost

    def part1(self, data: List[str]) -> int:
        """
        Consider the end point as (px, py), and the contributions from button A
        and B as (ax, ay) and (bx, by) respectively.

        The prize can be reached by pressing button A n times and button B m
        times, i.e.

        n*ax + m*bx = px [1],
        n*ay + m*by = py [2]

        We can then assert that:

        n = (py - m*by)/ay [3]

        by rearranging equation [2], and then inserting equation [3] into
        equation [1], we then derive m as follows

        ((py - m*by)/ay)*ax + m*bx = px [4]
        (py - m*by)*ax + m*bx = px [5]
        py*ax - m*by*ax + m*by*ay = py*ay [6]
        m = (px*ay - py*ax) / (bx*ay - by*ax) [7]

        Now we can solve for m, and then solve n with the value of m. We can
        assert that these values must be whole numbers to find a solution, then
        calculate the button cost.
        """
        cases = NewLineListParser(data).parse()
        prize_costs = []

        for case in cases:
            prize_costs.append(self.calculate_cost(case))

        return int(sum(prize_costs))

    def part2(self, data: List[str]) -> int:
        """Same as above, but add the extra offset to px/py which would break
        a BFS/DFS approach which the wording seems to be hinting at. Glad I
        did the analytical..."""
        cases = NewLineListParser(data).parse()
        prize_costs = []

        for case in cases:
            prize_costs.append(self.calculate_cost(case, prize_offset=10000000000000))

        return int(sum(prize_costs))


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day13(day, use_sample, run_each)
    solver.solve()
