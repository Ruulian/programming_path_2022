import requests
import re

url = "http://tournament.0xhorizon.eu:16776"

r = requests.post(url)

flag = re.findall(r"flag\{.+\}", r.text)[0]

print(flag)