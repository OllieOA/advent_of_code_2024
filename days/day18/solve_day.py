import heapq
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils import grid_utils


class Node:
    def __init__(
        self,
        parent=None,
        position: Tuple[int] = None,
        step: int = None,
    ):
        self.g_distance = 0
        self.h_heuristic = 0
        self.f_cost = 0

        self.parent = parent
        self.position = position
        self.step = step
        self.position_and_step = (position, step)

    def __eq__(self, other):
        return self.position_and_step == other.position_and_step

    def __repr__(self):
        return f"Position and Step: {self.position_and_step}, Total cost {self.f_cost} with g_distance {self.g_distance} and heuristic {self.h_heuristic}"

    def __lt__(self, other):
        return self.g_distance < other.g_distance

    def __gt__(self, other):
        return self.g_distance > other.g_distance


class Day18(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        if use_sample:
            self.grid_size = 6
            self.bytes_to_read = 12
        else:
            self.grid_size = 70
            self.bytes_to_read = 1024

    def generate_path(self, end_node: Node) -> List[Node]:
        path = []
        curr_node = end_node
        while curr_node is not None:
            path.append(curr_node)
            curr_node = curr_node.parent

        path.reverse()
        return path

    def do_maze(
        self,
        grid: np.array,
        start_pos: Tuple[int],
        end_pos: Tuple[int],
        enable_progress: bool = False,
    ) -> Tuple[List[Node], int]:
        start_node = Node(parent=None, position=start_pos, step=0)
        end_node = Node(parent=None, position=end_pos)

        open_list = []
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)
        closed_set = set([])
        open_node_lookup = {start_node.position: [start_node]}

        num_iters = 0

        while len(open_list) > 0:
            num_iters += 1
            curr_node = heapq.heappop(open_list)
            if num_iters % 500 == 0 and enable_progress:
                print(
                    f"Current distance from end {grid_utils.get_manhattan_dist(curr_node.position, end_node.position):03d}... ({num_iters/1000.0}k iters), length of open set {len(open_list)}, length of closed set {len(closed_set)}. Current node cost {curr_node.g_distance}",
                    end="\r",
                )
            closed_set.add(curr_node.position)
            open_node_lookup[curr_node.position].remove(curr_node)

            if curr_node.position == end_node.position:
                return self.generate_path(curr_node), curr_node.g_distance

            candidate_positions = grid_utils.get_adjacent_positions(
                curr_node.position, grid.shape, include_diagonals=False
            )

            candidates = []
            for candidate_pos in candidate_positions:
                if candidate_pos in closed_set:
                    continue
                if grid[candidate_pos] != ".":
                    continue
                candidate_node = Node(curr_node, candidate_pos, curr_node.step + 1)
                candidate_node.g_distance = curr_node.g_distance + 1
                candidate_node.h_heuristic = grid_utils.get_manhattan_dist(
                    candidate_pos, end_node.position
                )
                candidate_node.f_cost = candidate_node.g_distance + candidate_node.h_heuristic
                candidates.append(candidate_node)

            for candidate in candidates:
                # Here we only add to the heap if there is a node in the open list with a higher
                # path cost, if not - we can safely ignore it

                if candidate.position in open_node_lookup:
                    existing_nodes = open_node_lookup[candidate.position]
                    if any(o.g_distance <= candidate.g_distance for o in existing_nodes):
                        continue

                heapq.heappush(open_list, candidate)
                if candidate.position not in open_node_lookup:
                    open_node_lookup[candidate.position] = []
                open_node_lookup[candidate.position].append(candidate)
        return [], -1

    def part1(self, data: List[str]) -> int:
        corruption_bytes = []
        for line in data:
            corruption_bytes.append(tuple([int(x) for x in line.split(",")[::-1]]))

        grid = np.ones((self.grid_size + 1, self.grid_size + 1), dtype="str")
        grid[np.where(grid == "1")] = "."
        for corruption_byte in corruption_bytes[: self.bytes_to_read]:
            grid[corruption_byte] = "#"

        start_pos = (0, 0)
        end_pos = (self.grid_size, self.grid_size)

        _, length = self.do_maze(grid, start_pos=start_pos, end_pos=end_pos)
        return length

    def floodfill(self, grid: np.array, start_pos: Tuple[int], end_pos: Tuple[int]) -> bool:
        # Custom implementation to just check if the end node is in the flooded
        # set or not. My A* is doing something weird I guess

        visited = set([])
        check = [start_pos]
        while len(check) > 0:
            curr_node = check.pop(0)
            visited.add(curr_node)
            adj = grid_utils.get_adjacent_positions(curr_node, grid.shape, include_diagonals=False)

            for a in adj:
                if a in visited or a in check:
                    continue
                if grid[a] != ".":
                    continue
                check.append(a)

        return end_pos in visited

    def part2(self, data: List[str]) -> int:
        corruption_bytes = []
        for line in data:
            corruption_bytes.append(tuple([int(x) for x in line.split(",")[::-1]]))

        grid = np.ones((self.grid_size + 1, self.grid_size + 1), dtype="str")
        grid[np.where(grid == "1")] = "."

        start_pos = (0, 0)
        end_pos = (self.grid_size, self.grid_size)

        read_len = self.bytes_to_read
        accessible = True
        for corruption_byte in corruption_bytes[:read_len]:
            grid[corruption_byte] = "#"
        read_len -= 1
        while accessible:
            read_len += 1
            next_byte = corruption_bytes[read_len]
            grid[next_byte] = "#"

            accessible = self.floodfill(grid, start_pos, end_pos)

        target_byte = corruption_bytes[read_len]

        # 28,44 is correct
        return ",".join([str(x) for x in target_byte[::-1]])


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day18(day, use_sample, run_each)
    solver.solve()
