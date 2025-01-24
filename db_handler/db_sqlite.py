from db_handler.db_interface import DB
import sqlite3
from decouple import config
import os
import glob

class DBSqlite(DB):
    def __init__(self):
        self.connection = sqlite3.connect(config('SQLITE'))
        self.cursor = self.connection.cursor()

    def check_user(self, user: str) -> bool:
        self.cursor.execute("SELECT * from Users where user = ?", (user, ))
        if self.cursor.fetchall():
            return True
        return False

    def get_login_data(self, user: str) -> tuple[str, str]:
        self.cursor.execute("SELECT login, password from Users where user = ?", (user, ))
        return self.cursor.fetchall()[0]

    def set_login_data(self, user: str, login: str, password: str) -> bool:
        try:
            self.cursor.execute("INSERT INTO Users (user, login, password) VALUES (?,?,?)", (user, login, password))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_login_data(self, user: str, login: str, password: str) -> bool:
        try:
            self.cursor.execute("UPDATE (login, password) SET login = ?, password = ? WHERE user = ?", (login, password, user))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def delete_login_data(self, user: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM Users WHERE user = ?", (user, ))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def migrate_up(self, migrate_from: int = None, migrate_to: int = None) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "migrations", "sqlite")
        migration_files = [sql_file for sql_file in glob.glob(os.path.join(path, "up", "*.sql"))]
        if migrate_from is None:
            migrate_from = 0
        if migrate_to is None:
            migrate_to = len(migration_files)
        to_migrate = migration_files[migrate_from:migrate_to+1]
        for migration_file in to_migrate:
            with open(migration_file) as f:
                script = f.read()
                self.cursor.executescript(script)
        self.connection.commit()

    def migrate_down(self, migrate_from: int = None, migrate_to: int = None) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "migrations", "sqlite")
        migration_files = [sql_file for sql_file in glob.glob(os.path.join(path, "down", "*.sql"))]
        if migrate_from is None:
            migrate_from = len(migration_files)
        if migrate_to is None:
            migrate_to = 0
        to_migrate = migration_files[migrate_to:migrate_from+1]
        to_migrate = to_migrate[::-1]
        print(to_migrate)
        for migration_file in to_migrate:
            with open(migration_file) as f:
                script = f.read()
                self.cursor.executescript(script)
        self.connection.commit()