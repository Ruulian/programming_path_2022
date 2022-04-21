import os
import requests

flag = ""

with requests.get("https://tournament.0xhorizon.eu/some-lines/") as r:
    i = 1
    for line in r.text.split("\n"):
        line = line.strip("\n")
        if i % 17 == 0:
            flag += line
        i += 1

print(flag)