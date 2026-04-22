**Project Understanding Document**
=====================================

### 1. Project Summary

The AI-Powered Code Review Tool is a web-based application designed to automate code analysis, detect bugs, and identify code smells using Artificial Intelligence (AI) and Large Language Models (LLMs). The tool aims to reduce manual review time, enhance code quality, and improve collaboration among developers. It integrates with popular version control systems, allowing developers to seamlessly review and improve their code.

### 2. Key Technical Decisions

The following technical decisions were made for the project:

* **Backend:** Python with FastAPI was chosen for building the REST API due to its modern, fast, and high-performance capabilities.
* **Frontend:** Vanilla HTML/CSS/JS was chosen for the frontend due to its simplicity and ease of maintenance.
* **Database:** SQLite was chosen for storing user data and code analysis results due to its lightweight and easy-to-use nature.
* **LLM Integration:** Hugging Face Transformers library was chosen for integrating with Large Language Models due to its simplicity and efficiency.
* **Version Control System Integration:** GitHub and GitLab APIs were chosen for integrating with popular version control systems.

### 3. Critical Data Flows

The following are the 3-5 most important data flows in the application:

* **User Authentication:** The user sends a request to the `/api/v1/users/login` endpoint with their username and password. The application verifies the credentials and returns a JWT token if valid.
* **Repository Creation:** The user sends a request to the `/api/v1/repositories` endpoint with the repository name and URL. The application creates a new repository and returns the repository ID.
* **Code Analysis:** The user sends a request to the `/api/v1/repositories/{repository_id}/code-analysis` endpoint. The application runs the code analysis using the LLM and returns the results.
* **Issue Reporting:** The application sends a request to the `/api/v1/issues` endpoint with the issue details. The application creates a new issue and returns the issue ID.

### 4. API Highlights

The following are the most important endpoints and their purposes:

* **POST /api/v1/users:** Create a new user account.
* **POST /api/v1/users/login:** Login to an existing user account.
* **GET /api/v1/repositories:** Get a list of repositories for the authenticated user.
* **POST /api/v1/repositories:** Create a new repository.
* **GET /api/v1/repositories/{repository_id}/code-analysis:** Get the code analysis results for a repository.

### 5. Database Relationships

The following are the key table relationships and their business meaning:

* **Users:** Stores information about registered users.
* **Repositories:** Stores information about repositories for each user. A user can have multiple repositories (one-to-many).
* **Files:** Stores information about files in each repository. A repository can have multiple files (one-to-many).
* **Code_Analysis_Results:** Stores code analysis results for each repository. A repository can have multiple code analysis results (one-to-many).
* **Issues:** Stores issues found in the code analysis results. A code analysis result can have multiple issues (one-to-many).

### 6. Security Highlights

The following are the most important security measures to verify:

* **Authentication:** The application uses JWT tokens for authentication.
* **Authorization:** The application uses Role-Based Access Control (RBAC) to manage user permissions.
* **Input Validation:** The application validates all user input fields using predefined rules.
* **Token Expiration:** The application sets token expiration to 1 hour and provides a refresh token to obtain a new token when the current one expires.

### 7. Integration Points

The following are the integration points between the frontend, backend, and database:

* **Frontend-Backend:** The frontend sends requests to the backend API endpoints to perform actions such as user authentication, repository creation, and code analysis.
* **Backend-Database:** The backend interacts with the database to store and retrieve data such as user information, repository details, and code analysis results.

### 8. Audit Checklist

The following is the audit checklist for Phase 3:

* Verify that the application uses JWT tokens for authentication.
* Verify that the application uses RBAC to manage user permissions.
* Verify that the application validates all user input fields using predefined rules.
* Verify that the application sets token expiration to 1 hour and provides a refresh token to obtain a new token when the current one expires.
* Verify that the application integrates correctly with the version control systems (GitHub and GitLab).
* Verify that the application runs code analysis using the LLM and returns the results correctly.
* Verify that the application creates issues correctly and returns the issue ID.
* Verify that the application stores data correctly in the database.
* Verify that the application retrieves data correctly from the database.