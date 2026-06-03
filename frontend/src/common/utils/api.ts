import axios from 'axios';

// Base API configuration
export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 300000, // 5 minutes timeout (Gemini analysis can be slow)
});

// Interceptor for handling global errors (Rule 1.11, 2.13 concept)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // We can add global toast notifications or logging here
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
