import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Health check endpoint service
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/api/health');
    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED' || error.message.includes('Network Error') || !error.response) {
      throw new Error('Unable to connect to the prediction server. Please try again.');
    }
    throw error.response?.data?.error || 'Failed to check server health.';
  }
};

/**
 * Predict weight from height using Flask backend API
 * @param {number|string} height - Height in cm
 */
export const predictWeight = async (height) => {
  try {
    const response = await apiClient.post('/api/predict', { height: Number(height) });
    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED' || error.message?.includes('Network Error') || !error.response) {
      throw new Error('Unable to connect to the prediction server. Please try again.');
    }
    const backendMsg = error.response?.data?.error;
    throw new Error(backendMsg || 'Something went wrong. Please try again.');
  }
};
