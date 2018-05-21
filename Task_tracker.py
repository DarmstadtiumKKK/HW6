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

    def perform(self, id_task):
        point = self.db_connection.cursor()
        self.do_recursion(point, "per", id_task)
        self.db_connection.commit()
        point.close()

    def complete(self, id_task):
        point = self.db_connection.cursor()
        self.do_recursion(point, "com", id_task)
        self.db_connection.commit()
        point.close()

    def _same_actions(self, point, name, id_task):
        if name == "per":
            point.execute("UPDATE tasks SET status = %s, user_id = %s WHERE id = %s;", (2, self.user_id, id_task))
        else:
            point.execute("UPDATE tasks SET status = %s WHERE id = %s;", (3, id_task))
        point.execute("SELECT id FROM tasks WHERE id_parent = %s;", (id_task,))
        entries = point.fetchall()
        for task_id in entries:
            self.do_recursion(point, name, task_id)

    def get_status(self, id_task):
        point = self.db_connection.cursor()
        point.execute("SELECT status FROM tasks WHERE id = %s;", (id_task,))
        status = point.fetchone()
        point.close()
        return status[0]
