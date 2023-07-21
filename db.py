import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                      id INTEGER PRIMARY KEY,
                                      name TEXT NOT NULL,
                                      age INTEGER NOT NULL,
                                      email TEXT NOT NULL
                                  )''')
            logging.info("Table 'users' created if not exists.")
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def add_user(self, name, age, email):
        try:
            self.cursor.execute('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', (name, age, email))
            logging.info(f"User '{name}' added to the database.")
        except sqlite3.Error as e:
            logging.error(f"Error adding user: {e}")

    def get_all_users(self):
        try:
            self.cursor.execute('SELECT * FROM users')
            users = self.cursor.fetchall()
            logging.info("Retrieved all users from the database.")
            return users
        except sqlite3.Error as e:
            logging.error(f"Error retrieving users: {e}")
            return []

    def update_user(self, user_id, name, age, email):
        try:
            self.cursor.execute('UPDATE users SET name=?, age=?, email=? WHERE id=?', (name, age, email, user_id))
            logging.info(f"Updated information for user with ID={user_id}.")
        except sqlite3.Error as e:
            logging.error(f"Error updating user: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            logging.info(f"Deleted user with ID={user_id} from the database.")
        except sqlite3.Error as e:
            logging.error(f"Error deleting user: {e}")

if __name__ == "__main__":
    with UserDatabase() as db:
        db.create_table()

        db.add_user('Aliaksandr', 20, 'abbbbbbbbbbb@example.com')
        db.add_user('LuckyMan', 22, 'Lllllll@example.com')

        all_users = db.get_all_users()
        print("All Users:")
        for user in all_users:
            print(user)

        db.update_user(1, 'Aliaksandr True', 29, 'a.aaaaaaa@example.com')

        user_id_1 = db.get_all_users()[0]
        print("Updated User with ID=1:", user_id_1)

        db.delete_user(2)

        all_users_after_deletion = db.get_all_users()
        print("All Users after Deletion:")
        for user in all_users_after_deletion:
            print(user)
