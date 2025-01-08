import traceback
import sqlite3
from .config import logger, DATABASE_NAME



class Database():

    def __init__(self, db_name):
        self.connection = sqlite3.Connection(db_name)
        self.cursor = self.connection
        self.create_db()
    


    def create_db(self):
        try:
            query = (
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY, "
                "user_id BIGINT, "
                "username TEXT, "
                "first_name TEXT, "
                "last_name TEXT, "
                "complex TEXT, "
                "machine TEXT, "
                "member INTEGER DEFAULT 0);"
            )
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(f'Error in create_db: {e}')
            logger.error(f"{traceback.format_exc()}")



    def add_user(self, user_id, username, first_name, last_name):
        try:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            
            if not result.fetchone():
                self.cursor.execute(
                    "INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                    (user_id, username, first_name, last_name)
                )
                self.connection.commit()

        except Exception as e:
            logger.error(f'Error in add_user: {e}')
            logger.error(f"{traceback.format_exc()}")



    def update_user_data(self, user_id, complex_value, machine_value):
        try:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

            if result.fetchone():
                self.cursor.execute(
                    "UPDATE users SET complex = ?, machine = ? WHERE user_id = ?", 
                    (complex_value, machine_value, user_id)
                )
                self.connection.commit()
                
        except Exception as e:
            logger.error(f'Error in update_user_data: {e}')
            logger.error(f"{traceback.format_exc()}")
    


    def check_user(self, user_id):
        result = self.cursor.execute("SELECT complex, machine, member FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()
    

    def update_user_member(self, user_id):
        try:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

            if result.fetchone():
                self.cursor.execute(
                    "UPDATE users SET member = ? WHERE user_id = ?", 
                    (1, user_id)
                )
                self.connection.commit()
                
        except Exception as e:
            logger.error(f'Error in update_user_member: {e}')
            logger.error(f"{traceback.format_exc()}")
    
        



    def __del__(self):
        self.cursor.close()
        self.connection.close()



db = Database(DATABASE_NAME)