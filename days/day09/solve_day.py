from copy import deepcopy
from typing import List, Dict

from solver import Solver


class Day09(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day
        self.block_spec = {"id": -1, "blocks": [], "size": -1}

    def make_hdd(self, datablock: str) -> List[Dict]:
        space = False
        hdd = []

        curr_id = 0
        for n_str in datablock:
            curr_block_spec = deepcopy(self.block_spec)
            curr_block_spec["size"] = int(n_str)

            if not space:
                curr_block_spec["id"] = curr_id
                curr_block_spec["blocks"] = [curr_id] * int(n_str)
                curr_id += 1

            hdd.append(curr_block_spec)
            space = not space
        return hdd

    def get_checksum(self, hdd: List[Dict]) -> int:
        all_blocks = []
        for block in hdd:
            if len(block["blocks"]) == 0:
                all_blocks.extend([0] * block["size"])
            else:
                all_blocks.extend(block["blocks"])

        total_checksum = 0
        for idx, block_val in enumerate(all_blocks):
            total_checksum += idx * block_val
        return total_checksum

    def visualise_hdd(self, hdd: List[Dict]) -> None:
        all_blocks = []
        for block in hdd:
            if len(block["blocks"]) > 0:
                all_blocks.extend([str(x) for x in block["blocks"]])
            else:
                all_blocks.extend(["."] * block["size"])

        print("".join(all_blocks))

    def part1(self, data: List[str]) -> int:
        hdd = self.make_hdd(data[0])

        fwd_cursor = 0
        bkw_cursor = len(hdd) - 1

        while fwd_cursor < bkw_cursor:
            curr_fwd_block = hdd[fwd_cursor]
            if curr_fwd_block["id"] != -1:
                fwd_cursor += 1
                continue

            curr_end_block = hdd[bkw_cursor]
            while len(curr_fwd_block["blocks"]) < curr_fwd_block["size"]:
                if curr_end_block["id"] == -1 or len(curr_end_block["blocks"]) == 0:
                    bkw_cursor -= 1
                    curr_end_block = hdd[bkw_cursor]
                    continue
                curr_fwd_block["blocks"].append(curr_end_block["blocks"].pop(-1))
            fwd_cursor += 1

        return self.get_checksum(hdd)

    def part2(self, data: List[str]) -> int:
        hdd = self.make_hdd(data[0])

        bkw_cursor = len(hdd) - 1

        while bkw_cursor > 0:
            no_move = False
            if hdd[bkw_cursor]["id"] == -1:
                bkw_cursor -= 1
                continue

            target_size = hdd[bkw_cursor]["size"]
            fwd_cursor = 0
            while hdd[fwd_cursor]["size"] < target_size or hdd[fwd_cursor]["id"] != -1:
                fwd_cursor += 1
                if fwd_cursor > bkw_cursor:
                    no_move = True
                    break

            if no_move:
                bkw_cursor -= 1
                continue

            size_diff = hdd[fwd_cursor]["size"] - target_size

            if size_diff > 0:
                # We need to add in an extra piece of memory to compensate for
                # the "split" empty block
                _ = hdd.pop(fwd_cursor)  # Take it out at the start, because we
                # install a remainder block
                remainder_block = deepcopy(self.block_spec)
                remainder_block["size"] = size_diff
                hdd.insert(fwd_cursor, remainder_block)

                removed_memory = hdd.pop(bkw_cursor)
                move_replacement = deepcopy(self.block_spec)
                move_replacement["size"] = removed_memory["size"]
                hdd.insert(fwd_cursor, removed_memory)
                hdd.insert(bkw_cursor, move_replacement)
            else:
                removed_memory = hdd.pop(bkw_cursor)
                _ = hdd.pop(fwd_cursor)  # Here we take this out after removing
                # the memory, otherwise we will throw off the bkw_cursor
                move_replacement = deepcopy(self.block_spec)
                move_replacement["size"] = removed_memory["size"]

                hdd.insert(fwd_cursor, removed_memory)
                hdd.insert(bkw_cursor, move_replacement)

        return self.get_checksum(hdd)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day09(day, use_sample, run_each)
    solver.solve()
