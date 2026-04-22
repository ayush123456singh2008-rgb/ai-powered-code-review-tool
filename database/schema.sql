-- Drop existing tables if they exist
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Repositories;
DROP TABLE IF EXISTS Files;
DROP TABLE IF EXISTS Code_Analysis_Results;
DROP TABLE IF EXISTS Issues;

-- Create the Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create an index on the username column in the Users table
CREATE INDEX idx_Users_username ON Users (username);

-- Create the Repositories table
CREATE TABLE Repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the Files table
CREATE TABLE Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    repository_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the Code_Analysis_Results table
CREATE TABLE Code_Analysis_Results (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    repository_id INTEGER NOT NULL,
    analysis_date DATE NOT NULL,
    FOREIGN KEY (repository_id) REFERENCES Repositories (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create an index on the repository_id column in the Code_Analysis_Results table
CREATE INDEX idx_Code_Analysis_Results_repository_id ON Code_Analysis_Results (repository_id);

-- Create the Issues table
CREATE TABLE Issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    code_analysis_result_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    issue_type TEXT NOT NULL,
    issue_message TEXT NOT NULL,
    FOREIGN KEY (code_analysis_result_id) REFERENCES Code_Analysis_Results (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (file_id) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create an index on the file_id column in the Issues table
CREATE INDEX idx_Issues_file_id ON Issues (file_id);

-- Create a unique constraint on the username column in the Users table
CREATE UNIQUE INDEX uq_Users_username ON Users (username);

-- Create a unique constraint on the email column in the Users table
CREATE UNIQUE INDEX uq_Users_email ON Users (email);

-- Create a unique constraint on the url column in the Repositories table
CREATE UNIQUE INDEX uq_Repositories_url ON Repositories (url);

-- Create a check constraint to ensure that the analysis_date column in the Code_Analysis_Results table is not null
CREATE TABLE Code_Analysis_Results_Check (
    CHECK (analysis_date IS NOT NULL)
);

-- Insert the check constraint into the Code_Analysis_Results table
ALTER TABLE Code_Analysis_Results ADD CONSTRAINT chk_Code_Analysis_Results_analysis_date CHECK (analysis_date IS NOT NULL);