import httpClient from "../httpClient";

export async function getUser() {
    httpClient.get('/account', {})
    .then(response => {
        return response.data;
    })
    .catch(error => {
        console.log(error);
        return null;
    });
}
