import { TOKEN_STORAGE_KEY } from './constants.js';

const auth = {
  async login(username, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem(TOKEN_STORAGE_KEY, data.token);
        return data.token;
      } else {
        throw new Error(data.error.message);
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  },

  async register(username, password, email) {
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password, email }),
      });
      const data = await response.json();
      if (response.ok) {
        return data;
      } else {
        throw new Error(data.error.message);
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  },

  getToken() {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  },

  removeToken() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  },
};

export default auth;