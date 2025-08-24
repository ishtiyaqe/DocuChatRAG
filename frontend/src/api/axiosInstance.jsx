import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://192.168.0.109:8000',  // Replace with your Django backend URL
    timeout: 5000,
    headers: {
        'Authorization': localStorage.getItem('access_token')
            ? 'Bearer ' + localStorage.getItem('access_token')
            : null,
        'Content-Type': 'application/json',
        'accept': 'application/json',
    },
});


axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response.status === 401 && originalRequest.url === '/api/token/refresh/') {
            // Logout user and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login/';
            return Promise.reject(error);
        }

        if (error.response.data.code === 'token_not_valid' && error.response.status === 401) {
            const refreshToken = localStorage.getItem('refresh_token');

            if (refreshToken) {
                const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

                const now = Math.ceil(Date.now() / 1000);

                if (tokenParts.exp > now) {
                    return axiosInstance
                        .post('/api/token/refresh/', { refresh: refreshToken })
                        .then(response => {
                            localStorage.setItem('access_token', response.data.access);

                            axiosInstance.defaults.headers['Authorization'] =
                                'Bearer ' + response.data.access;

                            originalRequest.headers['Authorization'] =
                                'Bearer ' + response.data.access;

                            return axiosInstance(originalRequest);
                        })
                        .catch(err => {
                            console.log(err);
                        });
                } else {
                    console.log('Refresh token is expired', tokenParts.exp, now);
                    window.location.href = '/login/';
                }
            } else {
                console.log('Refresh token not available.');
                window.location.href = '/login/';
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
