import sqlite3
from sqlite3 import Error

class MigrationScript:
    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to SQLite database {self.db_name}")
        except Error as e:
            print(e)

    def create_migration_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            print("Migration table created")
        except Error as e:
            print(e)

    def create_users_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS Users
            """)
            cursor.execute("""
                CREATE TABLE Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_Users_username ON Users (username)
            """)
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_Users_username ON Users (username)
            """)
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_Users_email ON Users (email)
            """)
            self.conn.commit()
            print("Users table created")
        except Error as e:
            print(e)

    def create_repositories_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS Repositories
            """)
            cursor.execute("""
                CREATE TABLE Repositories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_Repositories_url ON Repositories (url)
            """)
            self.conn.commit()
            print("Repositories table created")
        except Error as e:
            print(e)

    def create_files_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS Files
            """)
            cursor.execute("""
                CREATE TABLE Files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    repository_id INTEGER NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            self.conn.commit()
            print("Files table created")
        except Error as e:
            print(e)

    def create_code_analysis_results_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS Code_Analysis_Results
            """)
            cursor.execute("""
                CREATE TABLE Code_Analysis_Results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    repository_id INTEGER NOT NULL,
                    analysis_date DATE NOT NULL,
                    FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_Code_Analysis_Results_repository_id ON Code_Analysis_Results (repository_id)
            """)
            cursor.execute("""
                ALTER TABLE Code_Analysis_Results ADD CONSTRAINT IF NOT EXISTS chk_Code_Analysis_Results_analysis_date CHECK (analysis_date IS NOT NULL)
            """)
            self.conn.commit()
            print("Code Analysis Results table created")
        except Error as e:
            print(e)

    def create_issues_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS Issues
            """)
            cursor.execute("""
                CREATE TABLE Issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    code_analysis_result_id INTEGER NOT NULL,
                    file_id INTEGER NOT NULL,
                    issue_type TEXT NOT NULL,
                    issue_message TEXT NOT NULL,
                    FOREIGN KEY (code_analysis_result_id) REFERENCES Code_Analysis_Results (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (file_id) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_Issues_file_id ON Issues (file_id)
            """)
            self.conn.commit()
            print("Issues table created")
        except Error as e:
            print(e)

    def up(self):
        self.create_migration_table()
        self.create_users_table()
        self.create_repositories_table()
        self.create_files_table()
        self.create_code_analysis_results_table()
        self.create_issues_table()

        # Insert migration record
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO migrations (name) VALUES ('initial_migration')
        """)
        self.conn.commit()

    def down(self):
        # Delete migration record
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM migrations WHERE name = 'initial_migration'
        """)
        self.conn.commit()

        # Drop tables in reverse order
        self.create_issues_table()
        cursor.execute("""
            DROP TABLE Issues
        """)
        self.create_code_analysis_results_table()
        cursor.execute("""
            DROP TABLE Code_Analysis_Results
        """)
        self.create_files_table()
        cursor.execute("""
            DROP TABLE Files
        """)
        self.create_repositories_table()
        cursor.execute("""
            DROP TABLE Repositories
        """)
        self.create_users_table()
        cursor.execute("""
            DROP TABLE Users
        """)
        self.create_migration_table()
        cursor.execute("""
            DROP TABLE migrations
        """)
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")

def main():
    db_name = "database.db"
    migration = MigrationScript(db_name)
    migration.create_connection()
    migration.up()
    # migration.down()  # Uncomment to roll back the migration
    migration.close_connection()

if __name__ == "__main__":
    main()