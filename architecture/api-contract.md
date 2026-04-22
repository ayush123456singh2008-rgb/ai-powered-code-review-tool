API Contract
================
## Base URL and Versioning Strategy
The base URL for the API is `https://api.ai-powered-code-review-tool.com/v1`. The API uses a versioning strategy based on the URL path.

## Authentication Scheme
The API uses JWT Bearer token authentication. All requests must include a valid JWT token in the `Authorization` header.

## Global Error Format
All error responses will be in the following format:
```json
{
  "error": {
    "code": <error_code>,
    "message": <error_message>
  }
}
```

## Rate Limiting Policy
The API has a rate limit of 100 requests per minute per IP address. Exceeding this limit will result in a 429 Too Many Requests error.

### Endpoints

#### 1. POST /api/v1/users
##### Description
Create a new user account.
##### Authentication
Required, JWT Bearer token
##### Request Body
```json
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```
##### Success Response
201 Created
```json
{
  "id": "integer",
  "username": "string",
  "email": "string"
}
```
##### Error Responses
* 400 Bad Request: Invalid request body
* 409 Conflict: Username already taken
##### Example Request/Response Pair
```bash
curl -X POST \
  https://api.ai-powered-code-review-tool.com/v1/users \
  -H 'Content-Type: application/json' \
  -d '{"username": "john", "password": "password123", "email": "john@example.com"}'
```
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com"
}
```

#### 2. POST /api/v1/users/login
##### Description
Login to an existing user account.
##### Authentication
Not required
##### Request Body
```json
{
  "username": "string",
  "password": "string"
}
```
##### Success Response
200 OK
```json
{
  "token": "string",
  "expires_in": "integer"
}
```
##### Error Responses
* 401 Unauthorized: Invalid username or password
* 404 Not Found: User not found
##### Example Request/Response Pair
```bash
curl -X POST \
  https://api.ai-powered-code-review-tool.com/v1/users/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "john", "password": "password123"}'
```
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "expires_in": 3600
}
```

#### 3. GET /api/v1/repositories
##### Description
Get a list of repositories for the authenticated user.
##### Authentication
Required, JWT Bearer token
##### Request Body
None
##### Success Response
200 OK
```json
[
  {
    "id": "integer",
    "name": "string",
    "url": "string"
  }
]
```
##### Error Responses
* 401 Unauthorized: Invalid token
* 404 Not Found: No repositories found
##### Example Request/Response Pair
```bash
curl -X GET \
  https://api.ai-powered-code-review-tool.com/v1/repositories \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
[
  {
    "id": 1,
    "name": "my-repo",
    "url": "https://github.com/john/my-repo"
  },
  {
    "id": 2,
    "name": "another-repo",
    "url": "https://github.com/john/another-repo"
  }
]
```

#### 4. POST /api/v1/repositories
##### Description
Create a new repository for the authenticated user.
##### Authentication
Required, JWT Bearer token
##### Request Body
```json
{
  "name": "string",
  "url": "string"
}
```
##### Success Response
201 Created
```json
{
  "id": "integer",
  "name": "string",
  "url": "string"
}
```
##### Error Responses
* 400 Bad Request: Invalid request body
* 409 Conflict: Repository already exists
##### Example Request/Response Pair
```bash
curl -X POST \
  https://api.ai-powered-code-review-tool.com/v1/repositories \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -d '{"name": "new-repo", "url": "https://github.com/john/new-repo"}'
```
```json
{
  "id": 3,
  "name": "new-repo",
  "url": "https://github.com/john/new-repo"
}
```

#### 5. GET /api/v1/repositories/{repository_id}/code-analysis
##### Description
Get the code analysis results for a repository.
##### Authentication
Required, JWT Bearer token
##### Request Body
None
##### Success Response
200 OK
```json
{
  "repository_id": "integer",
  "code_analysis_results": [
    {
      "file_name": "string",
      "issues": [
        {
          "type": "string",
          "message": "string"
        }
      ]
    }
  ]
}
```
##### Error Responses
* 401 Unauthorized: Invalid token
* 404 Not Found: Repository not found
##### Example Request/Response Pair
```bash
curl -X GET \
  https://api.ai-powered-code-review-tool.com/v1/repositories/1/code-analysis \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
{
  "repository_id": 1,
  "code_analysis_results": [
    {
      "file_name": "main.py",
      "issues": [
        {
          "type": "syntax_error",
          "message": "Invalid syntax on line 10"
        }
      ]
    }
  ]
}
```

#### 6. POST /api/v1/repositories/{repository_id}/code-analysis
##### Description
Run code analysis on a repository.
##### Authentication
Required, JWT Bearer token
##### Request Body
None
##### Success Response
202 Accepted
```json
{
  "repository_id": "integer",
  "code_analysis_status": "running"
}
```
##### Error Responses
* 401 Unauthorized: Invalid token
* 404 Not Found: Repository not found
##### Example Request/Response Pair
```bash
curl -X POST \
  https://api.ai-powered-code-review-tool.com/v1/repositories/1/code-analysis \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
{
  "repository_id": 1,
  "code_analysis_status": "running"
}
```