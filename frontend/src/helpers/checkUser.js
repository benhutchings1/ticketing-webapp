import httpClient from "../httpClient";

export function getUser() {
    let user;
    (async () => {
        try {
          const response = await fetch("http://localhost:5000/account");
          console.log(response);
          user = response.data;
        } catch (error) {
          user = null
        }
      })();

    return user;
}
