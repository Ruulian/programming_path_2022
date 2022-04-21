#!/usr/bin/env python3
import os
from string import printable
from random import choice, randint

chars = printable[:90].replace("!", "")

def gen_word(char=""):
    word = ""
    if char != "":
        word += "!"

    index = randint(10, 200)
    
    for i in range(index):
        word += choice(chars)
    
    word += char
    
    return word


flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()

print(flag)

with open(f"{os.path.abspath(os.path.dirname(__file__))}/file.txt", "a") as f:
    f.truncate(0)
    for char in flag:
        for i in range(randint(1, 100)):
            f.write(gen_word() + "\n")
        f.write(gen_word(char) + "\n")