from copy import deepcopy
from itertools import combinations, permutations
from typing import List, Dict, Tuple

from tqdm import tqdm

from solver import Solver
from utils.parsers import NewLineListParser


class Day24(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        if use_sample:
            self.pair_size = 4
        else:
            self.pair_size = 8

    def op_and(self, val1: bool, val2: bool) -> bool:
        return val1 and val2

    def op_or(self, val1: bool, val2: bool) -> bool:
        return val1 or val2

    def op_xor(self, val1: bool, val2: bool) -> bool:
        return val1 != val2

    def create_libraries(self, data: List[str]) -> None:
        bit_addresses, gates = NewLineListParser(data).parse()

        bit_library = {}
        for bit_spec in bit_addresses:
            bit_address, val = bit_spec.split(": ")
            bit_library[bit_address] = "1" == val

        op_library = []
        all_addresses = set([])
        for gate_spec in gates:
            operation_spec, target = gate_spec.split(" -> ")
            address_1, operation, address_2 = operation_spec.split(" ")
            all_addresses.update([address_1, address_2, target])
            op_library.append(
                {
                    "address_1": address_1,
                    "operation": operation,
                    "address_2": address_2,
                    "target": target,
                }
            )

        self.bit_library = bit_library
        self.op_library = op_library
        self.all_addresses = all_addresses

    def complete_libraries(self, op_library: List[Dict], bit_library: Dict) -> bool:
        last_set_diff = 0
        while len(self.all_addresses.difference(set(bit_library.keys()))) != 0:
            curr_set_diff = self.all_addresses.difference(set(bit_library.keys()))
            if last_set_diff == curr_set_diff:
                return False
            for op in op_library:
                addr1 = op["address_1"]
                addr2 = op["address_2"]
                target = op["target"]
                oper = op["operation"]

                if (not addr1 in bit_library.keys()) or (not addr2 in bit_library.keys()):
                    continue

                if target in bit_library.keys():
                    continue

                match oper:
                    case "AND":
                        bit_library[target] = self.op_and(bit_library[addr1], bit_library[addr2])
                    case "OR":
                        self.bit_library[target] = self.op_or(
                            bit_library[addr1], bit_library[addr2]
                        )
                    case "XOR":
                        self.bit_library[target] = self.op_xor(
                            bit_library[addr1], bit_library[addr2]
                        )
                    case "_":
                        raise ValueError(f"Unrecognized operation {oper}")
            last_set_diff = curr_set_diff
        return True

    def part1(self, data: List[str]) -> int:
        self.create_libraries(data)
        self.complete_libraries(self.op_library, self.bit_library)

        output_bit_addresses = sorted([x for x in list(self.all_addresses) if x.startswith("z")])
        output_bits = [self.bit_library[z] for z in output_bit_addresses]
        output_str = "".join(["1" if x else "0" for x in reversed(output_bits)])
        return int(output_str, 2)

    def check_system(self, bit_lib: Dict[str, bool]) -> bool:
        x_bit_addresses = sorted([x for x in list(self.all_addresses) if x.startswith("x")])
        y_bit_addresses = sorted([x for x in list(self.all_addresses) if x.startswith("y")])
        z_bit_addresses = sorted([x for x in list(self.all_addresses) if x.startswith("z")])

        x_bits = [bit_lib[x] for x in x_bit_addresses]
        y_bits = [bit_lib[y] for y in y_bit_addresses]
        z_bits = [bit_lib[z] for z in z_bit_addresses]

        x_val = int("".join("1" if x else "0" for x in reversed(x_bits)), 2)
        y_val = int("".join("1" if x else "0" for x in reversed(y_bits)), 2)
        z_val = int("".join("1" if x else "0" for x in reversed(z_bits)), 2)

        return (x_val + y_val) == z_val

    def part2(self, data: List[str]) -> None:
        self.create_libraries(data)
        # manual_bit_lib = {
        #     "x00": True,
        #     "x01": True,
        #     "x02": False,
        #     "x03": True,
        #     "y00": True,
        #     "y01": False,
        #     "y02": True,
        #     "y03": True,
        #     "z00": False,
        #     "z01": False,
        #     "z02": False,
        #     "z03": True,
        #     "z04": True,
        # }
        # self.all_addresses = set(manual_bit_lib.keys())
        # print(self.check_system(manual_bit_lib))
        # raise

        def assess_system(
            bit_library: Dict[str, bool], op_library: List[Dict], mix_spec: Tuple[int]
        ) -> Tuple[bool, Tuple[int]]:
            idx = 0

            target_mix_found = False
            while idx < len(mix_spec):
                p1 = mix_spec[idx]
                p2 = mix_spec[idx + 1]
                idx += 2

                p1_op_target = op_library[p1]["target"]
                p2_op_target = op_library[p2]["target"]
                op_library[p1]["target"] = p2_op_target
                op_library[p2]["target"] = p1_op_target

                if tuple(sorted([p1_op_target, p2_op_target])) != ("z00", "z05"):
                    target_mix_found = True

                # print(f"SWAPPING {p1_op_target} WITH {p2_op_target}")

            if not target_mix_found:
                return False, mix_spec

            possible = self.complete_libraries(op_library, bit_library)
            print(op_library)
            if not possible:
                print("NOT POSSIBLE")
                return False, mix_spec

            print("POSSIBLE, CHECKING CONSISTENCY...")
            return self.check_system(bit_library), mix_spec

        paired_target_indices = combinations(list(range(len(self.op_library))), self.pair_size)

        # for mix_spec in [(0, 1, 2, 3, 4, 5, 6, 7)]:
        for outer_mix_spec in tqdm(list(paired_target_indices)):
            for inner_mix_spec in permutations(outer_mix_spec, len(outer_mix_spec)):
                unsolved_bit_library = deepcopy(self.bit_library)
                unsolved_op_library = deepcopy(self.op_library)
                consistent, target_mix_spec = assess_system(
                    unsolved_bit_library, unsolved_op_library, inner_mix_spec
                )

                if consistent:
                    print("CONSISTENT")
                    raise
                    break
            if consistent:
                break

        print(target_mix_spec)
        swaps = [self.op_library[x]["target"] for x in target_mix_spec]

        return ",".join(sorted(swaps))


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day24(day, use_sample, run_each)
    solver.solve()
