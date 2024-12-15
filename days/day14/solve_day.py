from pathlib import Path
from typing import List, Dict

import cv2
import numpy as np

from solver import Solver


class Day14(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        if use_sample:
            self.height = 7
            self.width = 11
        else:
            self.height = 103
            self.width = 101

    def make_bots(self, data: List[str]) -> None:
        bots = []

        for spec in data:
            pos_spec, vel_spec = spec.replace("p=", "").replace("v=", "").split(" ", maxsplit=2)

            pos = [int(x) for x in pos_spec.split(",")]
            vel = tuple([int(x) for x in vel_spec.split(",")])

            bots.append({"pos": pos, "vel": vel})

        self.bots = bots

    def step_bots(self) -> None:
        for bot in self.bots:
            bot["pos"] = [p + v for p, v in zip(bot["pos"], bot["vel"])]
            if bot["pos"][0] >= self.width:
                bot["pos"][0] -= self.width
            elif bot["pos"][0] < 0:
                bot["pos"][0] += self.width

            if bot["pos"][1] >= self.height:
                bot["pos"][1] -= self.height
            elif bot["pos"][1] < 0:
                bot["pos"][1] += self.height

    def part1(self, data: List[str]) -> int:
        self.make_bots(data)
        for _ in range(100):
            self.step_bots()

        arr = np.zeros((self.height, self.width))
        for bot in self.bots:
            arr[(bot["pos"][1], bot["pos"][0])] += 1

        q1 = arr[: arr.shape[0] // 2, : arr.shape[1] // 2]
        q2 = arr[arr.shape[0] // 2 + 1 :, : arr.shape[1] // 2]
        q3 = arr[: arr.shape[0] // 2, arr.shape[1] // 2 + 1 :]
        q4 = arr[arr.shape[0] // 2 + 1 :, arr.shape[1] // 2 + 1 :]

        quadrants = [q1, q2, q3, q4]
        safety_factor = 1

        for q in quadrants:
            safety_factor *= int(np.sum(q))

        return safety_factor

    def part2(self, data: List[str]) -> None:
        self.make_bots(data)

        images_path = Path(__file__).parent / "inspection"
        images_path.mkdir(exist_ok=True)

        solved = False
        iters = 0
        while not solved:
            iters += 1
            self.step_bots()
            arr = np.zeros((self.height, self.width))
            for bot in self.bots:
                arr[(bot["pos"][1], bot["pos"][0])] += 1

            # Check if we have a line

            arr[np.where(arr > 0)] = 255
            img = arr.astype(np.uint8)
            lines = cv2.HoughLinesP(img, 1, np.pi / 180, 15, np.array([]), 5, 100)

            if lines is None:
                continue

            if len(lines) > 10:

                img_lines = np.copy(img)
                cv2.imwrite(str(images_path / f"check_base.png"), img)
                if lines is not None:
                    for line in lines:
                        for x1, x2, y1, y2 in line:
                            cv2.line(img_lines, (x1, y1), (x2, y2), (180, 0, 0))

                    cv2.imwrite(str(images_path / f"check_lines.png"), img_lines)

                response = input("Is it solved?")
                solved = "y" in response or "Y" in response

        return iters


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day14(day, use_sample, run_each)
    solver.solve()
