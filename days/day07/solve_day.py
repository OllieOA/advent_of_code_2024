from typing import List

from tqdm import tqdm

from solver import Solver


class BlankEquation:
    """This will do all the heavy lifting
    We first need to parse the lines, then we will generate a list of
    all possible equations based on the operators, and then check the solution
    of them. Really nothing crazy here.
    """

    def __init__(self, line: str, operators: List[str]) -> None:
        target, spec = line.split(": ")
        values = [int(x) for x in spec.split(" ")]

        self.target = target
        self.values = values
        self.operators = operators
        self._generate_all_equations()
        self.correct = self._check_any_true()

    def _generate_all_equations(self) -> None:
        curr_eqs = [[self.values[0]]]

        for idx, val in enumerate(self.values):
            new_eqs = []
            if idx == 0:
                continue

            for eq in curr_eqs:
                for op in self.operators:
                    new_eqs.append(eq + [(op, val)])

            curr_eqs = new_eqs

        self.eqs = curr_eqs

    def _check_any_true(self) -> bool:
        for eq in self.eqs:
            curr_eq_val = eq[0]
            for op in eq[1:]:
                if op[0] == "+":
                    curr_eq_val += op[1]
                elif op[0] == "*":
                    curr_eq_val *= op[1]
                elif op[0] == "||":
                    curr_eq_val = int(str(curr_eq_val) + str(op[1]))
                else:
                    raise ValueError(f"Something wrong with equation {eq}")

            if curr_eq_val == self.target:
                return True

        return False


class Day07(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        correct_vals = 0
        operators = ["*", "+"]
        for line in tqdm(data):
            eq = BlankEquation(line, operators)
            if eq.correct:
                correct_vals += eq.target

        return correct_vals

    def part2(self, data: List[str]) -> None:
        correct_vals = 0
        operators = ["*", "+", "||"]
        for line in tqdm(data):
            eq = BlankEquation(line, operators)
            if eq.correct:
                correct_vals += eq.target

        return correct_vals


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day07(day, use_sample, run_each)
    solver.solve()
