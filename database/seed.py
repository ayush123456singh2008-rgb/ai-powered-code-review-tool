import sqlite3
from datetime import date

def create_seed_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create seed data for the Users table
    users = [
        ('john_doe', 'password123', 'john@example.com'),
        ('jane_doe', 'password456', 'jane@example.com'),
        ('bob_smith', 'password789', 'bob@example.com'),
        ('alice_johnson', 'password012', 'alice@example.com'),
        ('charlie_brown', 'password345', 'charlie@example.com'),
    ]

    # Insert the seed data into the Users table
    cursor.executemany('''
        INSERT INTO Users (username, password, email)
        VALUES (?, ?, ?)
    ''', users)

    # Create seed data for the Repositories table
    repositories = [
        (1, 'my_repo', 'https://github.com/john_doe/my_repo'),
        (1, 'my_repo2', 'https://github.com/john_doe/my_repo2'),
        (2, 'janes_repo', 'https://github.com/jane_doe/janes_repo'),
        (3, 'bobs_repo', 'https://github.com/bob_smith/bobs_repo'),
        (4, 'alices_repo', 'https://github.com/alice_johnson/alices_repo'),
    ]

    # Insert the seed data into the Repositories table
    cursor.executemany('''
        INSERT INTO Repositories (user_id, name, url)
        VALUES (?, ?, ?)
    ''', repositories)

    # Create seed data for the Files table
    files = [
        (1, 'file1.txt', 'path/to/file1.txt'),
        (1, 'file2.txt', 'path/to/file2.txt'),
        (2, 'file3.txt', 'path/to/file3.txt'),
        (3, 'file4.txt', 'path/to/file4.txt'),
        (4, 'file5.txt', 'path/to/file5.txt'),
        (5, 'file6.txt', 'path/to/file6.txt'),
    ]

    # Insert the seed data into the Files table
    cursor.executemany('''
        INSERT INTO Files (repository_id, file_name, file_path)
        VALUES (?, ?, ?)
    ''', files)

    # Create seed data for the Code_Analysis_Results table
    code_analysis_results = [
        (1, date(2022, 1, 1)),
        (2, date(2022, 2, 1)),
        (3, date(2022, 3, 1)),
        (4, date(2022, 4, 1)),
        (5, date(2022, 5, 1)),
    ]

    # Insert the seed data into the Code_Analysis_Results table
    cursor.executemany('''
        INSERT INTO Code_Analysis_Results (repository_id, analysis_date)
        VALUES (?, ?)
    ''', code_analysis_results)

    # Create seed data for the Issues table
    issues = [
        (1, 1, 'error', 'This is an error message'),
        (1, 2, 'warning', 'This is a warning message'),
        (2, 3, 'error', 'This is another error message'),
        (3, 4, 'warning', 'This is another warning message'),
        (4, 5, 'error', 'This is yet another error message'),
    ]

    # Insert the seed data into the Issues table
    cursor.executemany('''
        INSERT INTO Issues (code_analysis_result_id, file_id, issue_type, issue_message)
        VALUES (?, ?, ?, ?)
    ''', issues)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == '__main__':
    create_seed_data()