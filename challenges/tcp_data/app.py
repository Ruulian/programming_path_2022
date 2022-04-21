#!/usr/bin/env python3

import os
import time

flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()
mdp = "g1ve_m3_th3_fl4g"

start = time.time()
recv = input("Quel est le mot de passe ? ")

if time.time() - start > 2:
    print("Trop tard :p")
elif recv == mdp:
    print(f"Bien joué voici ton flag: {flag}")
else:
    print("Mauvais mot de passe :(")