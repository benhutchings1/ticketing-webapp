import httpClient from "../httpClient";
import axios from "axios";

export async function getUser(token) {
    try {
        const requestOptions = {
            method: 'GET',
            credentials: 'same-origin',
            mode: 'cors',
            headers: {
                'Cookie': `access_token_cookie=${token}`,
                'Content-Type': 'application/json'
            }
        };

        console.log(requestOptions)
        const response = await fetch("http://localhost:5000/account", requestOptions)
        const userData = await response.json();

        console.log(userData);
        if (userData.email != null) {
            return userData;
        } else {
            return null;
        }
    } catch (error) {
        console.log(error)
        return null;
    }
}
