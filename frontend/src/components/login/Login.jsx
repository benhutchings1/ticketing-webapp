import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import "./login.css";
import {getUser} from "../../helpers/checkUser";
import {setAuthToken} from "../../helpers/setAuthToken";
import axios from "axios";

const Login = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loginError, setLoginError] = useState({});
    const [isSubmitted, setIsSubmitted] = useState(false);

    //temp database account info
    const database = [
      {
        email: "email1",
        password: "password1"
      }
    ];

    const errors = [
      {
        email: "invalid email",
        password: "invalid password"
      }
    ]

    const navigate = useNavigate();

    const logInUser = async () => {
        try {
            const data = {
                email_address: email,
                password: password
            }

            const requestOptions = {
                method: 'POST',
                mode: "cors",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            };

            const response = await fetch("http://localhost:5000/login", requestOptions)
            const userData = await response.json();

            console.log(userData);
            if (userData.success === true) {
                const token = userData.token;
                localStorage.setItem("access_token_cookie", token);
                setAuthToken(token);

                getUser(token).then(r => {
                    setUser(r);
                    navigate("/home");
                })
            }
        } catch (error) {
            alert(error)
        }
    };

    return (
        <div className='box'>
            <h1>LOGIN</h1>
            <div className='input-container'>
                    <label>Email: </label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        id="email"
                        name="email"
                        placeholder="youremail@gmail.com"
                        required
                    />
                </div>
                <div className='input-container'>
                    <label>Password: </label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        id="password"
                        name="password"
                        placeholder="********"
                        required
                    />
                </div>
                <div className='button-container'>
                  <button onClick={() => {logInUser()}}>Submit</button>
                </div>
            <button className='link-button' onClick={() => {navigate('/register')}}>Don't have an account? Register here</button>
        </div>
    )
};

export default Login;