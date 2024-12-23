from copy import deepcopy
from collections import Counter
from typing import List


from solver import Solver


class Day23(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def make_connections(self, data: List[str]) -> None:
        connections = {}
        for connection in data:
            n1, n2 = connection.split("-")
            if n1 not in connections:
                connections[n1] = set([])
            if n2 not in connections:
                connections[n2] = set([])
            connections[n1].add(n2)
            connections[n2].add(n1)

        self.connections = connections

    def part1(self, data: List[str]) -> int:
        self.make_connections(data)
        t_triads = set([])

        for n1 in self.connections:
            if not n1.startswith("t"):
                continue

            n1_connections = self.connections[n1]

            for n2 in n1_connections:
                n2_connections = self.connections[n2]
                interconnect_set = n2_connections.intersection(n1_connections)
                if len(interconnect_set) != 0:
                    for n3 in list(interconnect_set):
                        t_triads.add(tuple(sorted([n1, n2, n3])))

        return len(t_triads)

    def part2(self, data: List[str]) -> str:
        self.make_connections(data)

        self.networks = {}
        for k, v in self.connections.items():
            full_network = deepcopy(v)
            full_network.add(k)
            self.networks[k] = full_network

        max_len = 0
        max_network = []
        for s, max_nodes in self.networks.items():
            # For every start node, find everything it is connected to and then
            # filter that network

            all_sub_networks = []
            for node in list(max_nodes):
                all_sub_networks.append(
                    tuple(sorted(list(self.networks[node].intersection(max_nodes))))
                )

            all_sub_network_counts = Counter(all_sub_networks)

            max_interconnected_network, max_interconnected_count = (
                all_sub_network_counts.most_common()[0]
            )

            # If it is less than this (i.e. less than the full network length
            # minus the 2 checking nodes), it can't be a fully connected
            # solution
            if max_interconnected_count < (len(max_nodes) - 2):
                continue

            if len(max_interconnected_network) > max_len:
                max_network = max_interconnected_network
                max_len = len(max_network)

        return ",".join(max_network)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day23(day, use_sample, run_each)
    solver.solve()
