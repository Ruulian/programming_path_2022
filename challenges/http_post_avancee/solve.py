import requests
import re

url = "http://tournament.0xhorizon.eu:16775"

sess = requests.Session()

r = sess.post(url, data={"give":"cookie"})

flag = re.findall(r"flag\{.+\}", r.text)[0]

print(flag)