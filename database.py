import sqlite3
from random import randint, sample


def from_id(database, col, var):
    to_return = "SELECT * FROM " + str(database) + " WHERE " + str(col) + " = " + str(var)
    return to_return


def count(first, second, sign):
    if sign == "+":
        return first + second
    elif sign == "-":
        return first - second
    elif sign == "/":
        return first / second
    elif sign == "*":
        return first * second


def create_new(first, last, sign):
    if first > last:
        last, first = first, last
    fir = randint(first, last)
    sec = randint(first, last)
    result = count(fir, sec, sign)
    to_return = str(fir) + " " + str(sign) + " " + str(sec) + " = " + str(result)
    return to_return


# db = "MULTIPLY_EASIEST"
# col = "id"
# con = sqlite3.connect("db.sqlite3")
# cur = con.cursor()
# cur.execute("""CREATE TABLE MULTIPLY_EASIEST (
#               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#               to_count TEXT,
#               answer INTEGER);""")
# data = []
# for i in range(100):
#     first = randint(1, 9)
#    second = randint(1, 9)
#    adding = (str(first) + " * " + str(second) + " =", first * second)
#    data.append(adding)
# cur.executemany('INSERT INTO MULTIPLY_EASIEST (to_count, answer) values(?, ?)', data)


# con.commit()
# hm = sample(range(1, 101), 10)
# for i in hm:
#     print(cur.execute(from_id(db, col, i)).fetchone())

# for _ in range(10):
#    print(create_new(10, 30, "*"))


