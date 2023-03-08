import httpClient from "../httpClient";

export function getUser() {
    let user;
    (async () => {
        try {
          const response = await httpClient.get("//localhost:5000/@me");
          user = response.data;
        } catch (error) {
          user = null
        }
      })();

    return user;
}
