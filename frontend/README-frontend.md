# README-frontend.md
## Frontend Overview
The frontend of the AI-Powered Code Review Tool is built using modern web technologies, providing a seamless and intuitive user experience. The application allows users to easily navigate through the code review process, view analysis results, and collaborate with team members.

## Tech Stack Used
The following technologies are used in the frontend:
* **React**: A JavaScript library for building user interfaces
* **Redux**: A state management library for managing global state
* **Material-UI**: A UI framework for building responsive and consistent interfaces
* **JavaScript**: The primary programming language used for frontend development
* **CSS**: Used for styling and layout
* **HTML**: Used for structuring content

## File Structure
The frontend codebase is organized into the following folders:
* `public`: Contains static assets and index.html
* `src`: Contains the source code for the application
	+ `components`: Reusable UI components
	+ `containers`: Components that wrap around other components
	+ `actions`: Action creators for Redux
	+ `reducers`: Redux reducers for managing state
	+ `utils`: Utility functions for various tasks
	+ `index.js`: The main entry point for the application

## Setup Instructions
To set up the frontend project, follow these steps:
1. Clone the repository using `git clone`
2. Run `npm install` to install dependencies
3. Run `npm start` to start the development server

## Configuring the API Base URL
To configure the API base URL, create a new file named `.env` in the root of the project and add the following line:
```makefile
REACT_APP_API_BASE_URL=https://your-api-url.com
```
Replace `https://your-api-url.com` with the actual base URL of your API.

## Running Locally
To run the application locally, use the following command:
```bash
npm start
```
This will start the development server and make the application available at `http://localhost:3000`.

## Browser Compatibility
The application is compatible with the following browsers:
* Google Chrome (latest version)
* Mozilla Firefox (latest version)
* Microsoft Edge (latest version)
* Safari (latest version)

## Features Overview
The frontend of the AI-Powered Code Review Tool provides the following features:
* **Code Analysis**: View automated code analysis results, including bug detection and code smell identification
* **Review Workflows**: Customize review workflows to fit the needs of your team or organization
* **Collaboration**: Collaborate with team members on code reviews
* **Integration with Version Control Systems**: Integrate with popular version control systems, such as GitHub and GitLab
* **Responsive Design**: Access the application from any device, with a responsive design that adapts to different screen sizes.