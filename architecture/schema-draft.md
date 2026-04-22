# Database Schema for AI-Powered Code Review Tool
## Entity Overview
The following entities/tables will be used in the database schema:
* **Users**: stores information about registered users
* **Repositories**: stores information about repositories for each user
* **Code_Analysis_Results**: stores code analysis results for each repository
* **Issues**: stores issues found in the code analysis results
* **Files**: stores information about files in each repository

## Schema Tables
### Users Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| username | TEXT | NOT NULL, UNIQUE |
| password | TEXT | NOT NULL |
| email | TEXT | NOT NULL, UNIQUE |

### Repositories Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| user_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Users(id) |
| name | TEXT | NOT NULL |
| url | TEXT | NOT NULL, UNIQUE |

### Files Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| repository_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Repositories(id) |
| file_name | TEXT | NOT NULL |
| file_path | TEXT | NOT NULL |

### Code_Analysis_Results Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| repository_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Repositories(id) |
| analysis_date | DATE | NOT NULL |

### Issues Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| code_analysis_result_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Code_Analysis_Results(id) |
| file_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Files(id) |
| issue_type | TEXT | NOT NULL |
| issue_message | TEXT | NOT NULL |

## Indexes
* Create an index on the `username` column in the `Users` table for faster lookup
* Create an index on the `repository_id` column in the `Code_Analysis_Results` table for faster lookup
* Create an index on the `file_id` column in the `Issues` table for faster lookup

## Relationships
The relationships between the entities are as follows:
```markdown
+---------------+
|  Users      |
+---------------+
           |
           |
           v
+---------------+
|  Repositories  |
|  (one-to-many) |
+---------------+
           |
           |
           v
+---------------+
|  Files        |
|  (one-to-many) |
+---------------+
           |
           |
           v
+---------------+
|  Code_Analysis_Results |
|  (one-to-many)         |
+---------------+
           |
           |
           v
+---------------+
|  Issues      |
|  (many-to-one) |
+---------------+
```

## Sample Queries
Here are five sample queries that the app will need:
1. Get all repositories for a user: `SELECT * FROM Repositories WHERE user_id = ?`
2. Get all code analysis results for a repository: `SELECT * FROM Code_Analysis_Results WHERE repository_id = ?`
3. Get all issues for a file: `SELECT * FROM Issues WHERE file_id = ?`
4. Get all files for a repository: `SELECT * FROM Files WHERE repository_id = ?`
5. Get the user information for a given username: `SELECT * FROM Users WHERE username = ?`

## Migration Notes
To create the tables in the correct order, follow these steps:
1. Create the `Users` table
2. Create the `Repositories` table with a foreign key to the `Users` table
3. Create the `Files` table with a foreign key to the `Repositories` table
4. Create the `Code_Analysis_Results` table with a foreign key to the `Repositories` table
5. Create the `Issues` table with foreign keys to the `Code_Analysis_Results` and `Files` tables

Note: The above schema is designed based on the provided project brief, system design, and API contract. However, it's recommended to review and refine the schema as needed to ensure it meets the specific requirements of the project.