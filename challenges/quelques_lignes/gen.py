#!/usr/bin/env python3
import os
from string import printable
from random import choice, randint

chars = printable[:90]


flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()

print(flag)

with open(f"{os.path.abspath(os.path.dirname(__file__))}/file.txt", "a") as f:
    f.truncate(0)
    for char in flag:
        for i in range(16):
            f.write(choice(chars) + "\n")
        f.write(char + "\n")