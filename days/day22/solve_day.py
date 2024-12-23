from typing import List

from solver import Solver


class Day22(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.mod_val = 16777216

    def get_next_num(self, val: int) -> int:
        def mix_num(secret_num: int, mix_num: int) -> int:
            return secret_num ^ mix_num

        def prune_num(secret_num: int) -> int:
            return secret_num % self.mod_val

        # First step
        mod_val = val * 64
        val = mix_num(val, mod_val)
        val = prune_num(val)

        # Second step
        mod_val = val // 32
        val = mix_num(val, mod_val)
        val = prune_num(val)

        # Third step
        mod_val = val * 2048
        val = mix_num(val, mod_val)
        val = prune_num(val)

        return val

    def part1(self, data: List[str]) -> int:
        secret_nums = []
        for initial_num in data:
            val = int(initial_num)
            for _ in range(2000):
                val = self.get_next_num(val)
            secret_nums.append(val)

        return sum(secret_nums)

    def part2(self, data: List[str]) -> None:
        monkey_database = []
        print("Populating Monkey DB...")
        for initial_num in data:
            val = int(initial_num)
            monkey_sequence = [initial_num[-1]]
            diffs = []
            monkey_diff_sequences = {}
            for _ in range(2000):
                val = self.get_next_num(val)
                monkey_sequence.append(str(val)[-1])
                diffs.append(int(monkey_sequence[-1]) - int(monkey_sequence[-2]))

                if len(diffs) < 4:
                    continue
                diff_seq = tuple(diffs[-4:])
                if diff_seq in monkey_diff_sequences:
                    continue  # Will not reach this, monkey will choose the first
                monkey_diff_sequences[diff_seq] = int(monkey_sequence[-1])
            monkey_database.append(monkey_diff_sequences)

        print("Finding solution...")

        possible_sequences = set([])
        for db in monkey_database:
            possible_sequences.update(db.keys())

        best_val = 0

        for possible_seq in list(possible_sequences):
            possible_val = 0

            for db in monkey_database:
                possible_val += db.get(possible_seq, 0)

            if possible_val > best_val:
                best_val = possible_val

        return best_val


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day22(day, use_sample, run_each)
    solver.solve()
