#!/usr/bin/env python3

import os
import random
import time

flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()
a = random.randint(-100, 100)
b = random.randint(-100, 100)

x = round(b/a, 1)

print(f"{a}x = {b}\n")

start = time.time()
recv = input("x=")

try:
    if time.time() - start > 2:
        print("Trop tard :p")

    elif float(recv.strip("\n")) == x:
        print(f"Bien joué voici ton flag: {flag}")

    else:
        print("Mauvaise réponse :(")
except ValueError:
    print("Mauvaise réponse :(")
