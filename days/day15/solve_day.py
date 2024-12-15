from typing import List

import numpy as np

from solver import Solver
from utils import grid_utils
from utils.parsers import NewLineListParser, NumpyArrayParser


DIRECTIONS = {"<": (0, -1), ">": (0, 1), "v": (1, 0), "^": (-1, 0)}


class Day15(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def process_move(self, move: str) -> None:
        robot_pos = np.where(self.grid == "@")
        robot_pos = (int(robot_pos[0][0]), int(robot_pos[1][0]))

        move_tuple = DIRECTIONS[move]
        target_new_pos = grid_utils.get_tuple_in_direction(robot_pos, move_tuple)
        big_boxes_left = {
            (int(x), int(y)): (int(x), int(y + 1)) for x, y in zip(*np.where(self.grid == "["))
        }
        big_boxes_right = {
            (int(x), int(y)): (int(x), int(y - 1)) for x, y in zip(*np.where(self.grid == "]"))
        }

        match self.grid[target_new_pos]:
            case "#":  # Hitting a wall or column
                return
            case ".":  # Free space
                self.grid[robot_pos] = "."
                self.grid[target_new_pos] = "@"
            case "O":  # Box
                # Two minor cases - one is where there is a free space in the
                # line of boxes, and one where it all pushes against a wall
                box_free_space = target_new_pos
                while self.grid[box_free_space] == "O":
                    box_free_space = grid_utils.get_tuple_in_direction(
                        box_free_space, DIRECTIONS[move]
                    )

                non_box_space = self.grid[box_free_space]
                if non_box_space == "#":
                    return
                else:
                    self.grid[robot_pos] = "."
                    self.grid[target_new_pos] = "@"
                    self.grid[box_free_space] = "O"
            case "[" | "]":  # Bigger box
                box_path = []
                if self.grid[target_new_pos] == "[":
                    box_path.append(target_new_pos)
                    box_path.append(big_boxes_left[target_new_pos])
                else:
                    box_path.append(target_new_pos)
                    box_path.append(big_boxes_right[target_new_pos])

                l_boxes_to_move = set([])
                r_boxes_to_move = set([])
                can_move = True

                while len(box_path) > 0:
                    box_part = box_path.pop(0)
                    check_pos = grid_utils.get_tuple_in_direction(box_part, move_tuple)

                    if self.grid[box_part] == "]":
                        r_boxes_to_move.add(box_part)
                        if big_boxes_right[box_part] not in l_boxes_to_move:
                            box_path.append(big_boxes_right[box_part])
                    elif self.grid[box_part] == "[":
                        l_boxes_to_move.add(box_part)
                        if big_boxes_left[box_part] not in r_boxes_to_move:
                            box_path.append(big_boxes_left[box_part])

                    if self.grid[check_pos] in ["[", "]"] and (
                        check_pos not in l_boxes_to_move or check_pos not in r_boxes_to_move
                    ):
                        box_path.append(check_pos)

                    if self.grid[check_pos] == "#":
                        can_move = False
                        break

                    if self.grid[check_pos] == ".":
                        continue

                if not can_move:
                    return

                # Now we can move all of the boxes. r/l_boxes_to_move have sets
                # where boxes currently are, so first, we will clear the grid
                for pos in list(l_boxes_to_move.union(r_boxes_to_move)):
                    self.grid[pos] = "."

                for pos in list(l_boxes_to_move):
                    self.grid[grid_utils.get_tuple_in_direction(pos, move_tuple)] = "["
                for pos in list(r_boxes_to_move):
                    self.grid[grid_utils.get_tuple_in_direction(pos, move_tuple)] = "]"

                self.grid[robot_pos] = "."
                self.grid[grid_utils.get_tuple_in_direction(robot_pos, move_tuple)] = "@"
                return

    def get_score(self) -> int:
        total_score = 0
        if "O" in np.unique(self.grid):
            box_positions = [(int(x), int(y)) for x, y in zip(*np.where(self.grid == "O"))]
        else:
            box_positions = [(int(x), int(y)) for x, y in zip(*np.where(self.grid == "["))]

        for box_pos in box_positions:
            total_score += 100 * box_pos[0] + box_pos[1]

        return total_score

    def part1(self, data: List[str]) -> int:
        grid_spec, moves = NewLineListParser(data).parse()

        self.grid = NumpyArrayParser(grid_spec).parse()
        moveset = "".join(moves)

        for move in moveset:
            self.process_move(move)

        return self.get_score()

    def part2(self, data: List[str]) -> None:
        grid_spec, moves = NewLineListParser(data).parse()
        new_grid_spec = []

        spec_lookup = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@.",
        }

        for line in grid_spec:
            new_line = ""
            for spec in line:
                new_line += spec_lookup[spec]
            new_grid_spec.append(new_line)

        moveset = "".join(moves)

        self.grid = NumpyArrayParser(new_grid_spec).parse()

        for move in moveset:
            self.process_move(move)

        return self.get_score()


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day15(day, use_sample, run_each)
    solver.solve()
