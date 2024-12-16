import heapq
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils import grid_utils
from utils.parsers import NumpyArrayParser


HEADING_TO_TUPLE = {
    0: (0, 1),
    90: (-1, 0),
    180: (0, -1),
    270: (1, 0),
}


class Node:
    def __init__(
        self,
        parent: Tuple[Tuple[int], int] = None,
        position: Tuple[int] = None,
        heading: int = None,
    ):
        self.g_distance = 0
        self.h_heuristic = 0
        self.f_cost = 0

        self.parent = parent
        self.position = position
        self.heading = heading
        self.position_and_heading = (position, heading)

    def __eq__(self, other):
        return self.position_and_heading == other.position_and_heading

    def __repr__(self):
        return f"Position and Heading: {self.position_and_heading}, Total cost {self.f_cost} with g_distance {self.g_distance} and heuristic {self.h_heuristic}"

    def __lt__(self, other):
        return self.g_distance < other.g_distance

    def __gt__(self, other):
        return self.g_distance > other.g_distance


class Day16(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day
        self.best_cost = 0

    def generate_path(self, end_node: Node) -> List[Node]:
        path = []
        curr_node = end_node
        while curr_node is not None:
            path.append(curr_node)
            curr_node = curr_node.parent

        path.reverse()
        return path

    def do_maze(
        self, grid: np.array, start_pos: Tuple[int], end_pos: Tuple[int]
    ) -> Tuple[List[Node], int]:
        start_node = Node(parent=None, position=start_pos, heading=0)
        end_node = Node(parent=None, position=end_pos)

        open_list = []
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)
        closed_set = set([])

        num_iters = 0

        while len(open_list) > 0:
            num_iters += 1

            curr_node = heapq.heappop(open_list)
            if num_iters % 500 == 0:
                print(
                    f"Current distance from end {grid_utils.get_manhattan_dist(curr_node.position, end_node.position):03d}... ({num_iters/1000.0}k iters)",
                    end="\r",
                )
            closed_set.add(curr_node.position_and_heading)

            if curr_node.position == end_node.position:
                return self.generate_path(curr_node), curr_node.g_distance

            # Get possible next positions
            candidate_headings = [
                curr_node.heading - 90 if (curr_node.heading - 90) >= 0 else 270,
                curr_node.heading + 90 if (curr_node.heading + 90) < 360 else 0,
            ]
            pre_cost_candidates = [
                Node(curr_node, position=curr_node.position, heading=h) for h in candidate_headings
            ]

            candidates = []

            for candidate in pre_cost_candidates:
                step_pos_candidate = grid_utils.get_tuple_in_direction(
                    curr_node.position, HEADING_TO_TUPLE[candidate.heading]
                )
                if grid[step_pos_candidate] in [".", "E"]:
                    candidate.g_distance = curr_node.g_distance + 1000  # Rotations are expensive
                    candidates.append(candidate)

            curr_heading_tuple = HEADING_TO_TUPLE[curr_node.heading]
            step_pos = grid_utils.get_tuple_in_direction(curr_node.position, curr_heading_tuple)
            if (
                step_pos[0] >= 0
                and step_pos[0] < grid.shape[0]
                and step_pos[1] >= 0
                and step_pos[1] < grid.shape[1]
                and grid[step_pos] in [".", "E"]
            ):
                step_node = Node(curr_node, position=step_pos, heading=curr_node.heading)
                step_node.g_distance = curr_node.g_distance + 1
                candidates.append(step_node)

            for candidate in candidates:
                candidate.h_heuristic = grid_utils.get_manhattan_dist(
                    candidate.position, end_node.position
                )
                candidate.f_cost = candidate.g_distance + candidate.h_heuristic

            for candidate in candidates:
                if candidate.position_and_heading in closed_set:
                    continue
                # Here we only add to the heap if there is a node in the open list with a higher
                # path cost, if not - we can safely ignore it
                if (
                    len(
                        [
                            o
                            for o in open_list
                            if candidate.position_and_heading == o.position_and_heading
                            and candidate.g_distance > o.g_distance
                        ]
                    )
                    > 0
                ):
                    continue
                heapq.heappush(open_list, candidate)

    def part1(self, data: List[str]) -> int:
        grid = NumpyArrayParser(data).parse()

        start_pos = np.where(grid == "S")
        start_pos = (int(start_pos[0][0]), int(start_pos[1][0]))

        end_pos = np.where(grid == "E")
        end_pos = (int(end_pos[0][0]), int(end_pos[1][0]))

        _, cost = self.do_maze(grid, start_pos, end_pos)

        self.best_cost = cost
        return cost

    def get_all_path_at_cost(
        self, grid: np.array, start_pos: Tuple[int], end_pos: Tuple[int], max_cost: int
    ) -> List[List[Node]]:
        # TODO: Refactor this with do_maze() to remove duplicated code
        paths_at_cost = []

        start_node = Node(parent=None, position=start_pos, heading=0)
        end_node = Node(parent=None, position=end_pos)

        open_list = []
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)
        closed_set = set([])

        while len(open_list) > 0:
            curr_node = heapq.heappop(open_list)
            if curr_node.g_distance > max_cost:
                continue
            closed_set.add(curr_node.position_and_heading)

            if curr_node.position == end_node.position:
                paths_at_cost.append(self.generate_path(curr_node))

            # Get possible next positions
            candidate_headings = [
                curr_node.heading - 90 if (curr_node.heading - 90) >= 0 else 270,
                curr_node.heading + 90 if (curr_node.heading + 90) < 360 else 0,
            ]
            pre_cost_candidates = [
                Node(curr_node, position=curr_node.position, heading=h) for h in candidate_headings
            ]

            candidates = []

            for candidate in pre_cost_candidates:
                step_pos_candidate = grid_utils.get_tuple_in_direction(
                    curr_node.position, HEADING_TO_TUPLE[candidate.heading]
                )
                if grid[step_pos_candidate] in [".", "E"]:
                    candidate.g_distance = curr_node.g_distance + 1000  # Rotations are expensive
                    candidates.append(candidate)

            curr_heading_tuple = HEADING_TO_TUPLE[curr_node.heading]
            step_pos = grid_utils.get_tuple_in_direction(curr_node.position, curr_heading_tuple)
            if (
                step_pos[0] >= 0
                and step_pos[0] < grid.shape[0]
                and step_pos[1] >= 0
                and step_pos[1] < grid.shape[1]
                and grid[step_pos] in [".", "E"]
            ):
                step_node = Node(curr_node, position=step_pos, heading=curr_node.heading)
                step_node.g_distance = curr_node.g_distance + 1
                candidates.append(step_node)

            for candidate in candidates:
                candidate.h_heuristic = grid_utils.get_manhattan_dist(
                    candidate.position, end_node.position
                )
                candidate.f_cost = candidate.g_distance + candidate.h_heuristic

            for candidate in candidates:
                if candidate.position_and_heading in closed_set:
                    continue
                # Here we only add to the heap if there is a node in the open list with a higher
                # path cost, if not - we can safely ignore it
                if (
                    len(
                        [
                            o
                            for o in open_list
                            if candidate.position_and_heading == o.position_and_heading
                            and candidate.g_distance > o.g_distance
                        ]
                    )
                    > 0
                ):
                    continue
                heapq.heappush(open_list, candidate)
        return paths_at_cost

    def part2(self, data: List[str]) -> int:
        grid = NumpyArrayParser(data).parse()

        start_pos = np.where(grid == "S")
        start_pos = (int(start_pos[0][0]), int(start_pos[1][0]))

        end_pos = np.where(grid == "E")
        end_pos = (int(end_pos[0][0]), int(end_pos[1][0]))

        if self.best_cost == 0:
            _, best_cost = self.do_maze(grid, start_pos, end_pos)
            self.best_cost = best_cost

        # Now we can go through and find all possible paths that match this
        # cost

        all_paths_at_cost = self.get_all_path_at_cost(grid, start_pos, end_pos, self.best_cost)

        tiles_on_path = set([])
        for path in all_paths_at_cost:
            for node in path:
                tiles_on_path.add(node.position)

        return len(tiles_on_path)

        # return len(path)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day16(day, use_sample, run_each)
    solver.solve()
