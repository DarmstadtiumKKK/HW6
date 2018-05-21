from MySQLdb import NULL
from faker import Faker
from Task_tracker import Bound
import random

fake = Faker()

con = Bound("root", "12345", "task_tracker")


class FillingDB:
    def __init__(self, db_connection, num):
        self.db_connection = db_connection.connection
        c = self.db_connection.cursor()
        c.execute("SELECT MIN(id) from tasks;")
        tup = c.fetchone()
        self.begin = tup[0]
        c.execute("SELECT MAX(id) from tasks;")
        tup = c.fetchone()
        self.end = tup[0]
        self.num = num
        c.close()

    # Генератор, который возвращает tuple ,где первый параметр это условие вложенности, а второй id_parent от min до max
    def gen_random(self):
        for _ in range(self.num):
            yield (random.randint(0, 1), random.randint(self.begin, self.end))

    def fill_tasks(self):
        c = self.db_connection.cursor()

        for rand in self.gen_random():

            if rand[0] and self.end:

                c.execute("INSERT INTO tasks (status, id_parent) VALUES (%s, %s);", (1, rand[1]))
            else:
                c.execute("INSERT INTO tasks (status) VALUES (%s);", (1,))

            # При каждом добавлении задачи увеличиваем дипазон рандома на еденицу
            self.end += 1

        self.db_connection.commit()

    def fill_users(self):
        c = self.db_connection.cursor()
        for _ in range(self.num):
            c.execute("INSERT INTO users (name) VALUES (%s);", (fake.name(),))
        self.db_connection.commit()


with con:
    fill = FillingDB(con, 10)
    fill.fill_tasks()
    fill.fill_users()