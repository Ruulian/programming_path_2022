import requests
import re

url = "http://tournament.0xhorizon.eu:16777"

r = requests.get(url)

flag = re.findall(r"flag\{.+\}", r.text)[0]

print(flag)