import axios from "axios";

const API_ROUTE_URL = process.env.REACT_APP_ROUTE_URL || "https://localhost:5000";

const httpClient = axios.create({
    withCredentials: true,
    baseURL: API_ROUTE_URL,
});

httpClient.interceptors.response.use(response => {
    return response.data;
}, error => {
    return Promise.reject(error);
});

export default httpClient;