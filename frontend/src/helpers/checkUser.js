import httpClient from "../httpClient";

export async function getUser(setUser) {
    httpClient.get(`/user/account`, {})
    .then((response) => {
        setUser(response);
        return response;
    })
    .catch(error => {
        setUser(null);
        return null;
    });
}

export function isUserLoggedIn(user) {
    return (user !== null && user.firstname !== undefined);
}