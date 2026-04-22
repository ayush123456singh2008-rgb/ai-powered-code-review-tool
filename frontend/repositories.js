import api from './api.js';
import { TOKEN_STORAGE_KEY } from './constants.js';

const repositories = {
  async getAll() {
    try {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      const response = await api.get('/repositories', token);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },

  async create(name, url) {
    try {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      const response = await api.post('/repositories', { name, url }, token);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },

  async getCodeAnalysis(repositoryId) {
    try {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      const response = await api.get(`/repositories/${repositoryId}/code-analysis`, token);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },

  async runCodeAnalysis(repositoryId) {
    try {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      const response = await api.post(`/repositories/${repositoryId}/code-analysis`, null, token);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },
};

export default repositories;