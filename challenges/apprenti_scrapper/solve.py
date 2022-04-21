import requests
import re
from bs4 import BeautifulSoup as bs

url = "http://tournament.0xhorizon.eu:16778/"

sess = requests.Session()

r1 = sess.post(url, data={"go":""})

soup = bs(r1.text, 'html.parser')
questions = soup.find_all("div", {"class":"accordion-body"})

for_q3 = str(questions[2]).split("id: ")[1].split("\n")[0].replace(" ", "")
for_q4 = str(questions[3]).split("classe ")[1].split("\n")[0].replace(" ", "")
for_q5 = str(questions[4]).split("contenu ")[1].split("\n")[0].replace(" ", "")

r = sess.get(f"{url}challenge/")

soup = bs(r.text, 'html.parser')
title = soup.find("title").contents[0]
span = soup.find_all("span")[15].contents[0]
first_child = list(soup.find("div", attrs={"id":for_q3}).children)[1].attrs['id']
by_class = soup.find_all(attrs={"class":for_q4})[-2].attrs['id']
by_content = soup.find("a", text=for_q5).attrs['id']

answer = sess.post(f"{url}answer/", 
    {
        "question1":title,
        "question2":span,
        "question3":first_child,
        "question4":by_class,
        "question5":by_content
    }
)
print(answer.text)