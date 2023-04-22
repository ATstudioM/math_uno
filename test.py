import sqlite3
from random import randint


def need_math():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    db = 'easiest'
    hm = randint(1, 100)
    cur.execute("SELECT * FROM " + db + " WHERE id=" + str(hm))
    print(cur.fetchone())

need_math()