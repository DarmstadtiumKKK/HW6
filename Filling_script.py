from MySQLdb import NULL
from faker import Faker
from Bounding_class import Bound
import random

fake = Faker()

con = Bound("root", "12345", "task_tracker")


class FillingDB:
    def __init__(self, db_connection, num):
        self.db_connection = db_connection.connection
        point = self.db_connection.cursor()
        point.execute("SELECT MIN(id) from tasks;")
        tup = point.fetchone()
        self.begin = tup[0]
        point.execute("SELECT MAX(id) from tasks;")
        tup = point.fetchone()
        self.end = tup[0]
        self.num = num
        point.close()

    def gen_random(self):
        for _ in range(self.num):
            yield (random.randint(0, 1), random.randint(self.begin, self.end))

    def fill_tasks(self):
        point = self.db_connection.cursor()
        for rand in self.gen_random():
            if rand[0] and self.end:
                point.execute("INSERT INTO tasks (status, id_parent) VALUES (%s, %s);", (1, rand[1]))
            else:
                point.execute("INSERT INTO tasks (status) VALUES (%s);", (1,))
            self.end += 1

        self.db_connection.commit()
        point.close()

    def fill_users(self):
        point = self.db_connection.cursor()
        for _ in range(self.num):
            point.execute("INSERT INTO users (name) VALUES (%s);", (fake.name(),))
        self.db_connection.commit()
        point.close()


with con:
    fill = FillingDB(con, 10)
    fill.fill_tasks()
    fill.fill_users()
