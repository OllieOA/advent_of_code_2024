from typing import List

from solver import Solver
from utils.parsers import NewLineListParser


class Day17(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def combo(self, val: int) -> int:
        match val:
            case 0 | 1 | 2 | 3:
                return val
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise ValueError("Should not get a combo operator of 7!")

    def adv(self, operand: int) -> None:
        self.a = int(self.a / (2 ** self.combo(operand)))
        self.inst_ptr += 2

    def bxl(self, operand: int) -> None:
        self.b = self.b ^ operand
        self.inst_ptr += 2

    def bst(self, operand: int) -> None:
        self.b = self.combo(operand) % 8
        self.inst_ptr += 2

    def jnz(self, operand: int) -> None:
        if self.a == 0:
            self.inst_ptr += 2
            return

        self.inst_ptr = operand

    def bxc(self) -> None:
        self.b = self.b ^ self.c
        self.inst_ptr += 2

    def out(self, operand: int) -> str:
        self.inst_ptr += 2
        return str(self.combo(operand) % 8)

    def bdv(self, operand: int) -> None:
        self.b = int(self.a / (2 ** self.combo(operand)))
        self.inst_ptr += 2

    def cdv(self, operand: int) -> None:
        self.c = int(self.a / (2 ** self.combo(operand)))
        self.inst_ptr += 2

    def run_program(self) -> int:
        self.inst_ptr = 0
        output_vals = []
        num_iters = 0
        while self.inst_ptr < len(self.op_codes):
            num_iters += 1
            if num_iters % 1 == 0:
                print(f"Instruction pointer at {self.inst_ptr}/{len(self.op_codes)}")
            next_opcode = self.op_codes[self.inst_ptr]
            next_operand = self.op_codes[self.inst_ptr + 1]
            match next_opcode:
                case 0:
                    self.adv(next_operand)
                case 1:
                    self.bxl(next_operand)
                case 2:
                    self.bst(next_operand)
                case 3:
                    self.jnz(next_operand)
                case 4:
                    self.bxc()
                case 5:
                    output_vals.append(self.out(next_operand))
                case 6:
                    self.bdv(next_operand)
                case 7:
                    self.cdv(next_operand)

        return ",".join(output_vals)

    def part1(self, data: List[str]) -> int:
        registers_spec, program_spec = NewLineListParser(data).parse()

        self.registers = {"A": 0, "B": 0, "C": 0}
        for register in registers_spec:
            register = register.replace("Register ", "")
            target_register, target_value = register.split(": ", maxsplit=2)
            self.registers[target_register] = int(target_value)

        self.a = self.registers["A"]
        self.b = self.registers["B"]
        self.c = self.registers["C"]

        self.op_codes = [int(x) for x in program_spec[0].replace("Program: ", "").split(",")]

        return self.run_program()

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day17(day, use_sample, run_each)
    solver.solve()
