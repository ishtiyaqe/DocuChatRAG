import axios from 'axios';
import Cookies from 'js-cookie';

// Function to get CSRF token from cookies
const getCsrfToken = () => Cookies.get('csrftoken');
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,  // Change to your Django backend URL
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken(),
  },
});

export default api;
