from hashlib import md5
import json
import sqlite3
from collections import defaultdict
import os

DB_PATH = "/var/databases/prog_tournament.sqlite"
SALT = ",ZYod9Qk*5e_+QO"

def group_list(list_to_sort:list):
    d = defaultdict(list)
    for k, *v in list_to_sort:
        d[k].append(v)
    return list(d.items())

def hasher(password:str):
    string = SALT + password
    return md5(string.encode()).hexdigest()

class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.init_db()

    
    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    # Database conf
    def create_table(self, table):
        name = table["name"]
        cols = ", ".join([f"{i['name']} {i['type']} {i['options']}" for i in table["columns"]])
        
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {name}({cols})"
        )
        self.conn.commit()
        

    def insert_challenge(self, id, name, category, points, flag, url, description, hint, published):
        self.cur.execute(
            "insert or ignore into challenges(id, name, category, points, flag, url, description, hint, published) values(:id, :name, :category, :points, :flag, :url, :description, :hint, :published)",
            {
                "id":id,
                "name":name,
                "category":category,
                "points":points,
                "flag":flag,
                "url":url,
                "description":description,
                "hint":hint,
                "published":published
            }
        )
        self.conn.commit()

    def init_db(self):
        self.cur.execute("DROP TABLE IF EXISTS challenges")
        self.conn.commit()

        with open(f"{os.path.abspath(os.path.dirname(__file__))}/db.json", "r") as db:
            j = json.loads(db.read())
        
        for table in j["tables"]:
            self.create_table(table)
        for chall in j["challenges"]:
            self.insert_challenge(chall["id"], chall["name"], chall["category"], chall["points"], chall["flag"], chall["url"], chall["description"], chall["hint"], 1)

    # User interaction
    def register(self, first_name, last_name, username, password):

        self.cur.execute(
            "INSERT INTO users(name, username, password) VALUES(:name, :username, :password)",
            {
                "name":f"{first_name} {last_name}",
                "username":username,
                "password":hasher(password)
            }
        )

        self.conn.commit()
        

    def check_username(self, username):

        res = list(
            self.cur.execute(
                "SELECT * FROM users WHERE username=:username",
                {
                    "username":username
                }
            )
        )
        

        if res == []:
            return True
        else:
            return False

    def check_login(self, username, password):

        res = list(
            self.cur.execute(
                "SELECT id FROM users WHERE username=:username AND password=:password",
                {
                    "username":username,
                    "password":hasher(password)
                }
            )
        )
        

        if res != []:
            return True
        else:
            return False

    def check_flag(self, flag_submitted, challenge_id):

        res = list(
            self.cur.execute(
                "SELECT * FROM challenges WHERE id=:id AND flag=:flag",
                {
                    "id":challenge_id,
                    "flag":flag_submitted
                }
            )
        )
        
        
        if res == []:
            return False
        return True


    # Solves
    def add_solve(self, user, chall_id, points):

        self.cur.execute(
            "INSERT INTO solves(username, chall_id, points) VALUES(:username, :chall_id, :points)",
            {
                "username":user,
                "chall_id":chall_id,
                "points":points
            }
        )

        self.conn.commit()
        

    def check_solve(self, user, chall_id):

        res = list(
            self.cur.execute(
                "SELECT * FROM solves WHERE username=:username AND chall_id=:chall_id",
                {
                    "username":user,
                    "chall_id":chall_id
                }
            )
        )
        

        if res == []:
            return False
        return True


    # User informations
    def get_points(self, username):

        res = list(
            self.cur.execute(
                "SELECT COALESCE(SUM(points),0) FROM solves WHERE username=:username",
                {
                    "username":username
                }
            )
        )
        
        
        
        if res == []:
            return 0
        return res[0][0]

    # Challenges informations
    def get_challenges_points(self, chall_id):
    
        initial_points = list(
            self.cur.execute(
                "SELECT points FROM challenges WHERE id=:id",
                {
                    "id":chall_id
                }
            )
        )[0][0]
    
        solves = list(
            self.cur.execute(
                "SELECT * FROM solves WHERE chall_id=:chall_id",
                {
                    "chall_id":chall_id
                }
            )
        )
        nb = len(solves)
    
        
        
        return initial_points - nb

    # Global infos
    def get_leaderboard(self):

        res = list(
            self.cur.execute(
                "SELECT ROW_NUMBER () OVER ( ORDER BY (select COALESCE(sum(points),0) from solves where username=users.username) DESC) RowNum, username, (select COALESCE(SUM(points),0) FROM solves WHERE username=users.username) AS points FROM users ORDER BY points DESC",
            )
        )
        
        

        return res

    def get_challenges(self, user):

        res = list(
            self.cur.execute(
                "SELECT category, id, name, points, url, description, hint, CASE WHEN (SELECT username FROM solves WHERE chall_id=id) = :username THEN 'solved' ELSE 'default' END as validated FROM challenges WHERE published=1 ORDER BY category",
                {
                    "username":user
                }
            )
        )
    
        

        return group_list(res)

    # Manager
    def start_contest(self):

        self.cur.execute(
            "UPDATE challenges SET published=1"
        )
        self.conn.commit()
    
    def stop_contest(self):

        self.cur.execute(
            "UPDATE challenges SET published=0"
        )
        self.conn.commit()

    def down(self, chall_id):

        self.cur.execute(
            "UPDATE challenges SET published=0 WHERE id=:chall_id",
            {
                "chall_id":chall_id
            }
        )
        self.conn.commit()
    
    def up(self, chall_id):

        self.cur.execute(
            "UPDATE challenges SET published=1 WHERE id=:chall_id",
            {
                "chall_id":chall_id
            }
        )
        self.conn.commit()

    def drop(self, table):
        self.cur.execute(
            f"DROP TABLE {table}"
        )
        self.conn.commit()