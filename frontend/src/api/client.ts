import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8011';

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export default api;
