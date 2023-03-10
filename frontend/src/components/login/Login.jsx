import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import "./login.css";

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

    const logInUser = async (event) => {
        console.log(email, password);
        event.preventDefault();

        try {
              const resp = await httpClient.post("//localhost:5000/login", {
                  email,
                  password,
              });
              navigate("/home")

        } catch (error) {
            if (error.response.status === 401) {
                alert("Invalid credentials");
            }
        }
    };

    return (
        <div className='box'>
            <h1>Login</h1>
            <form className="login-form" onSubmit={logInUser}>
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
                  <button type="submit">
                      Submit
                  </button>
                </div>
            </form>
            <button className='link-button' onClick={() => {navigate('/register')}}>Don't have an account? Register here</button>
        </div>
    )
};

export default Login;