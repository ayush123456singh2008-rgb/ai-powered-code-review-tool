import auth from './auth.js';
import repositories from './repositories.js';

const app = {
  async init() {
    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        // Token is valid, load repositories
        const repositoriesList = await repositories.getAll();
        this.renderRepositoriesList(repositoriesList);
      } else {
        // No token, show login form
        this.renderLoginForm();
      }
    } catch (error) {
      console.error(error);
    }
  },

  renderLoginForm() {
    const loginFormHtml = `
      <form id="login-form">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username"><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>
        <button type="submit">Login</button>
      </form>
    `;
    document.body.innerHTML = loginFormHtml;

    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      try {
        const token = await auth.login(username, password);
        // Token is valid, load repositories
        const repositoriesList = await repositories.getAll();
        this.renderRepositoriesList(repositoriesList);
      } catch (error) {
        console.error(error);
      }
    });
  },

  renderRepositoriesList(repositoriesList) {
    const repositoriesListHtml = `
      <h1>Repositories</h1>
      <ul id="repositories-list">
        ${repositoriesList.map((repository) => `<li>${repository.name}</li>`).join('')}
      </ul>
      <button id="create-repository-button">Create Repository</button>
    `;
    document.body.innerHTML = repositoriesListHtml;

    const createRepositoryButton = document.getElementById('create-repository-button');
    createRepositoryButton.addEventListener('click', async () => {
      try {
        const name = prompt('Enter repository name:');
        const url = prompt('Enter repository URL:');
        const response = await repositories.create(name, url);
        // Repository created, reload list
        const newRepositoriesList = await repositories.getAll();
        this.renderRepositoriesList(newRepositoriesList);
      } catch (error) {
        console.error(error);
      }
    });

    const repositoriesListElement = document.getElementById('repositories-list');
    repositoriesListElement.addEventListener('click', async (e) => {
      if (e.target.tagName === 'LI') {
        const repositoryId = e.target.dataset.id;
        try {
          const codeAnalysis = await repositories.getCodeAnalysis(repositoryId);
          this.renderCodeAnalysis(codeAnalysis);
        } catch (error) {
          console.error(error);
        }
      }
    });
  },

  renderCodeAnalysis(codeAnalysis) {
    const codeAnalysisHtml = `
      <h1>Code Analysis</h1>
      <pre>${JSON.stringify(codeAnalysis, null, 2)}</pre>
      <button id="run-code-analysis-button">Run Code Analysis</button>
    `;
    document.body.innerHTML = codeAnalysisHtml;

    const runCodeAnalysisButton = document.getElementById('run-code-analysis-button');
    runCodeAnalysisButton.addEventListener('click', async () => {
      try {
        const repositoryId = codeAnalysis.repository_id;
        const response = await repositories.runCodeAnalysis(repositoryId);
        // Code analysis running, reload list
        const newCodeAnalysis = await repositories.getCodeAnalysis(repositoryId);
        this.renderCodeAnalysis(newCodeAnalysis);
      } catch (error) {
        console.error(error);
      }
    });
  },
};

app.init();