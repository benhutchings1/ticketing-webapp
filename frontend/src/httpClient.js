import axios from "axios";

const httpClient = axios.create({
    withCredentials: true,
    baseURL: 'http://localhost:5000',
});

httpClient.interceptors.response.use(response => {
    if (response.config.user) {

    }
    return response.data;
}, error => {
    return Promise.reject(error);
});

export default httpClient;