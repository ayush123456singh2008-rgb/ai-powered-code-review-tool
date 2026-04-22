# Database Overview
The database is designed to store information about users, repositories, files, code analysis results, and issues. It provides a structured way to manage data related to code analysis and issue tracking.

## Schema Description
The database consists of five tables: Users, Repositories, Files, Code_Analysis_Results, and Issues.

*   **Users Table:**
    *   `id`: Unique identifier for each user.
    *   `username`: Unique username chosen by the user.
    *   `password`: Password for the user's account.
    *   `email`: Unique email address associated with the user's account.
*   **Repositories Table:**
    *   `id`: Unique identifier for each repository.
    *   `user_id`: Foreign key referencing the Users table, indicating the repository's owner.
    *   `name`: Name of the repository.
    *   `url`: Unique URL of the repository.
*   **Files Table:**
    *   `id`: Unique identifier for each file.
    *   `repository_id`: Foreign key referencing the Repositories table, indicating the file's repository.
    *   `file_name`: Name of the file.
    *   `file_path`: Path to the file within the repository.
*   **Code_Analysis_Results Table:**
    *   `id`: Unique identifier for each code analysis result.
    *   `repository_id`: Foreign key referencing the Repositories table, indicating the repository analyzed.
    *   `analysis_date`: Date when the code analysis was performed.
*   **Issues Table:**
    *   `id`: Unique identifier for each issue.
    *   `code_analysis_result_id`: Foreign key referencing the Code_Analysis_Results table, indicating the analysis that detected the issue.
    *   `file_id`: Foreign key referencing the Files table, indicating the file where the issue was found.
    *   `issue_type`: Type of issue detected (e.g., bug, security vulnerability).
    *   `issue_message`: Description of the issue.

## Setup Instructions
To set up the database, follow these steps:

1.  Install a compatible database management system (e.g., SQLite).
2.  Create a new database or use an existing one.
3.  Execute the provided SQL script to create the tables and relationships.

## How to Run Migrations
To apply changes to the database schema, follow these steps:

1.  Create a new migration script with the necessary changes (e.g., adding a new table or column).
2.  Execute the migration script against the database.

## How to Seed Data
To populate the database with initial data, follow these steps:

1.  Create a seed script with INSERT statements for the desired data.
2.  Execute the seed script against the database.

## Query Examples
Here are some example queries:

*   Retrieve all users: `SELECT * FROM Users;`
*   Retrieve all repositories for a specific user: `SELECT * FROM Repositories WHERE user_id = ?;`
*   Retrieve all files in a specific repository: `SELECT * FROM Files WHERE repository_id = ?;`
*   Retrieve all code analysis results for a specific repository: `SELECT * FROM Code_Analysis_Results WHERE repository_id = ?;`
*   Retrieve all issues detected in a specific file: `SELECT * FROM Issues WHERE file_id = ?;`

## Index Optimization Notes
Indexes have been created on the following columns to improve query performance:

*   `Users.username`
*   `Code_Analysis_Results.repository_id`
*   `Issues.file_id`
*   Unique constraints have been created on the `Users.username`, `Users.email`, and `Repositories.url` columns to ensure data consistency.

## Backup Strategy
To ensure data safety, implement a regular backup strategy:

1.  Schedule daily backups of the database using a tool like `sqlite3 .backup main backup.db`.
2.  Store backup files in a secure location, such as an external hard drive or cloud storage service.
3.  Test backup files periodically to ensure they can be restored successfully in case of data loss.