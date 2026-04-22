import sqlite3
from typing import List, Dict, Tuple

class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Files (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                repository_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Code_Analysis_Results (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                repository_id INTEGER NOT NULL,
                analysis_date DATE NOT NULL,
                FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                code_analysis_result_id INTEGER NOT NULL,
                file_id INTEGER NOT NULL,
                issue_type TEXT NOT NULL,
                issue_message TEXT NOT NULL,
                FOREIGN KEY (code_analysis_result_id) REFERENCES Code_Analysis_Results (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (file_id) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    # CRUD operations for Users table
    def create_user(self, username: str, password: str, email: str) -> int:
        try:
            self.cursor.execute('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None

    def get_user(self, user_id: int) -> Dict:
        try:
            self.cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
            user = self.cursor.fetchone()
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[3]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting user: {e}")
            return None

    def update_user(self, user_id: int, username: str, email: str) -> bool:
        try:
            self.cursor.execute('UPDATE Users SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False

    # CRUD operations for Repositories table
    def create_repository(self, user_id: int, name: str, url: str) -> int:
        try:
            self.cursor.execute('INSERT INTO Repositories (user_id, name, url) VALUES (?, ?, ?)', (user_id, name, url))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating repository: {e}")
            return None

    def get_repository(self, repository_id: int) -> Dict:
        try:
            self.cursor.execute('SELECT * FROM Repositories WHERE id = ?', (repository_id,))
            repository = self.cursor.fetchone()
            if repository:
                return {
                    'id': repository[0],
                    'name': repository[2],
                    'url': repository[3]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting repository: {e}")
            return None

    def update_repository(self, repository_id: int, name: str, url: str) -> bool:
        try:
            self.cursor.execute('UPDATE Repositories SET name = ?, url = ? WHERE id = ?', (name, url, repository_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating repository: {e}")
            return False

    def delete_repository(self, repository_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM Repositories WHERE id = ?', (repository_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting repository: {e}")
            return False

    # CRUD operations for Files table
    def create_file(self, repository_id: int, file_name: str, file_path: str) -> int:
        try:
            self.cursor.execute('INSERT INTO Files (repository_id, file_name, file_path) VALUES (?, ?, ?)', (repository_id, file_name, file_path))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating file: {e}")
            return None

    def get_file(self, file_id: int) -> Dict:
        try:
            self.cursor.execute('SELECT * FROM Files WHERE id = ?', (file_id,))
            file = self.cursor.fetchone()
            if file:
                return {
                    'id': file[0],
                    'repository_id': file[1],
                    'file_name': file[2],
                    'file_path': file[3]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting file: {e}")
            return None

    def update_file(self, file_id: int, file_name: str, file_path: str) -> bool:
        try:
            self.cursor.execute('UPDATE Files SET file_name = ?, file_path = ? WHERE id = ?', (file_name, file_path, file_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating file: {e}")
            return False

    def delete_file(self, file_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM Files WHERE id = ?', (file_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting file: {e}")
            return False

    # CRUD operations for Code_Analysis_Results table
    def create_code_analysis_result(self, repository_id: int, analysis_date: str) -> int:
        try:
            self.cursor.execute('INSERT INTO Code_Analysis_Results (repository_id, analysis_date) VALUES (?, ?)', (repository_id, analysis_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating code analysis result: {e}")
            return None

    def get_code_analysis_result(self, code_analysis_result_id: int) -> Dict:
        try:
            self.cursor.execute('SELECT * FROM Code_Analysis_Results WHERE id = ?', (code_analysis_result_id,))
            code_analysis_result = self.cursor.fetchone()
            if code_analysis_result:
                return {
                    'id': code_analysis_result[0],
                    'repository_id': code_analysis_result[1],
                    'analysis_date': code_analysis_result[2]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting code analysis result: {e}")
            return None

    def update_code_analysis_result(self, code_analysis_result_id: int, analysis_date: str) -> bool:
        try:
            self.cursor.execute('UPDATE Code_Analysis_Results SET analysis_date = ? WHERE id = ?', (analysis_date, code_analysis_result_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating code analysis result: {e}")
            return False

    def delete_code_analysis_result(self, code_analysis_result_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM Code_Analysis_Results WHERE id = ?', (code_analysis_result_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting code analysis result: {e}")
            return False

    # CRUD operations for Issues table
    def create_issue(self, code_analysis_result_id: int, file_id: int, issue_type: str, issue_message: str) -> int:
        try:
            self.cursor.execute('INSERT INTO Issues (code_analysis_result_id, file_id, issue_type, issue_message) VALUES (?, ?, ?, ?)', (code_analysis_result_id, file_id, issue_type, issue_message))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating issue: {e}")
            return None

    def get_issue(self, issue_id: int) -> Dict:
        try:
            self.cursor.execute('SELECT * FROM Issues WHERE id = ?', (issue_id,))
            issue = self.cursor.fetchone()
            if issue:
                return {
                    'id': issue[0],
                    'code_analysis_result_id': issue[1],
                    'file_id': issue[2],
                    'issue_type': issue[3],
                    'issue_message': issue[4]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting issue: {e}")
            return None

    def update_issue(self, issue_id: int, issue_type: str, issue_message: str) -> bool:
        try:
            self.cursor.execute('UPDATE Issues SET issue_type = ?, issue_message = ? WHERE id = ?', (issue_type, issue_message, issue_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating issue: {e}")
            return False

    def delete_issue(self, issue_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM Issues WHERE id = ?', (issue_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting issue: {e}")
            return False

    # Join queries
    def get_repositories_with_files(self, user_id: int) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT r.id, r.name, r.url, f.file_name, f.file_path
                FROM Repositories r
                JOIN Files f ON r.id = f.repository_id
                WHERE r.user_id = ?
            ''', (user_id,))
            repositories = self.cursor.fetchall()
            if repositories:
                return [
                    {
                        'id': repository[0],
                        'name': repository[1],
                        'url': repository[2],
                        'file_name': repository[3],
                        'file_path': repository[4]
                    } for repository in repositories
                ]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error getting repositories with files: {e}")
            return []

    def get_code_analysis_results_with_issues(self, repository_id: int) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT c.id, c.analysis_date, i.issue_type, i.issue_message
                FROM Code_Analysis_Results c
                JOIN Issues i ON c.id = i.code_analysis_result_id
                WHERE c.repository_id = ?
            ''', (repository_id,))
            code_analysis_results = self.cursor.fetchall()
            if code_analysis_results:
                return [
                    {
                        'id': code_analysis_result[0],
                        'analysis_date': code_analysis_result[1],
                        'issue_type': code_analysis_result[2],
                        'issue_message': code_analysis_result[3]
                    } for code_analysis_result in code_analysis_results
                ]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error getting code analysis results with issues: {e}")
            return []

    # Search/filter queries
    def search_users(self, username: str) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM Users WHERE username LIKE ?', (f'%{username}%',))
            users = self.cursor.fetchall()
            if users:
                return [
                    {
                        'id': user[0],
                        'username': user[1],
                        'email': user[3]
                    } for user in users
                ]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error searching users: {e}")
            return []

    def search_repositories(self, name: str) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM Repositories WHERE name LIKE ?', (f'%{name}%',))
            repositories = self.cursor.fetchall()
            if repositories:
                return [
                    {
                        'id': repository[0],
                        'name': repository[2],
                        'url': repository[3]
                    } for repository in repositories
                ]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error searching repositories: {e}")
            return []

    # Pagination support
    def get_repositories_paginated(self, user_id: int, page: int, per_page: int) -> List[Dict]:
        try:
            offset = (page - 1) * per_page
            self.cursor.execute('''
                SELECT r.id, r.name, r.url
                FROM Repositories r
                WHERE r.user_id = ?
                LIMIT ? OFFSET ?
            ''', (user_id, per_page, offset))
            repositories = self.cursor.fetchall()
            if repositories:
                return [
                    {
                        'id': repository[0],
                        'name': repository[1],
                        'url': repository[2]
                    } for repository in repositories
                ]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error getting repositories paginated: {e}")
            return []

# Example usage:
db = Database('database.db')
db.create_tables()

# Create a new user
user_id = db.create_user('john', 'password123', 'john@example.com')
print(f"User ID: {user_id}")

# Create a new repository
repository_id = db.create_repository(user_id, 'my-repo', 'https://github.com/john/my-repo')
print(f"Repository ID: {repository_id}")

# Get a list of repositories for the user
repositories = db.get_repositories_with_files(user_id)
print("Repositories:")
for repository in repositories:
    print(repository)

# Create a new code analysis result
code_analysis_result_id = db.create_code_analysis_result(repository_id, '2022-01-01')
print(f"Code Analysis Result ID: {code_analysis_result_id}")

# Get a list of code analysis results with issues
code_analysis_results = db.get_code_analysis_results_with_issues(repository_id)
print("Code Analysis Results:")
for code_analysis_result in code_analysis_results:
    print(code_analysis_result)

# Search for users
users = db.search_users('john')
print("Users:")
for user in users:
    print(user)

# Search for repositories
repositories = db.search_repositories('my-repo')
print("Repositories:")
for repository in repositories:
    print(repository)

# Get a list of repositories paginated
repositories = db.get_repositories_paginated(user_id, 1, 10)
print("Repositories:")
for repository in repositories:
    print(repository)

db.close_connection()