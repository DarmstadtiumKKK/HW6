import MySQLdb


class Bound:
    def __init__(self, user, password, db, host='localhost'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)

    def disconnect(self):
        if self._connection:
            self._connection.close()


class TaskTracker:
    def __init__(self, db_bound, user_id):
        self.db_connection = db_bound.connection
        self.user_id = user_id
        self.dict_of_status = {1: 'new_task', 2: 'perform', 3: 'completed'}

    def add_task(self, id_parent=None):
        point = self.db_connection.cursor()
        if id_parent is not None:
            point.execute("INSERT INTO tasks (status, id_parent) VALUES (%s, %s);", (1, id_parent))
        else:
            point.execute("INSERT INTO tasks (status) VALUES (%s);", (1,))
        self.db_connection.commit()
        point.close()

    def do_recursion(self,point,func):
        point.execute("SELECT id FROM tasks WHERE id_parent = %s;", (id_task,))
        entries = point.fetchall()
        self.db_connection.commit()
        point.close()
        for task_id in entries:
            func(task_id)

    def perform(self, id_task):
        point = self.db_connection.cursor()
        point.execute("UPDATE tasks SET status = %s, user_id = %s WHERE id = %s;",(2, self.user_id, id_task))
        self.do_recursion(point, self.perform)

    def complete(self, id_task):
        point = self.db_connection.cursor()
        point.execute("UPDATE tasks SET status = %s WHERE id = %s;", (3, id_task))
        self.do_recursion(point, self.complete)

    def get_status(self, id_task):
        point = self.db_connection.cursor()
        point.execute("SELECT status FROM tasks WHERE id = %s;", (id_task,))
        status = point.fetchone()
        point.close()
        return status[0]


con = Bound("root", "12345", "task_tracker")

with con:
    task = TaskTracker(con, 22)
    # task.add_task()
    # task.perform(4)
    task.complete(19)
    print(task.get_status(19))