import os
import requests

flag = ""

with requests.get("https://tournament.0xhorizon.eu/special-lines/") as r:
    for line in r.text.split("\n"):
        line = line.strip("\n")
        if line[0] == "!":
            flag += line[-1]

print(flag)