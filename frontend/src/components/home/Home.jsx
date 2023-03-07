import React, {useEffect, useState} from 'react'
import httpClient from "../../httpClient";
import { User } from "../../types";
import {useNavigate} from "react-router-dom";

const Home = () => {
  const [user, setUser] = useState(null);

  const navigate = useNavigate();

  const logoutUser = async () => {
    await httpClient.post("//localhost:5000/logout");
    navigate("/")
  };

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/@me");
        setUser(resp.data);
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

  return (
    <div>
      <h1>Welcome to e-ticketing!</h1>
      {user != null ? (
        <div>
          <h2>Logged in</h2>
          <h3>ID: {user.id}</h3>
          <h3>Email: {user.email}</h3>

          <button onClick={logoutUser}>Logout</button>
        </div>
      ) : (
        <div>
          <p>You are not logged in</p>
          <div>
            <button onClick={() => {navigate('/login')}}>Login</button>
            <button onClick={() => {navigate('/register')}}>Register</button>
          </div>
        </div>
      )}
    </div>
  )
};

export default Home;