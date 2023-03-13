import "./login.css";

import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../helpers";
import { element } from "prop-types";

const Login = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loginError, setLoginError] = useState("");


    const navigate = useNavigate();

    const logInUser = async (event) => {
        event.preventDefault();
        
        const data = {
            email_address: email,
            password: password
        }
 
        httpClient.post('/login', data)
        .then(response => {
        getUser(setUser).then(r => {
            navigate("/home");
        })
        })
        .catch(error => {
        console.log(error.response.data);
        if (error.response && error.response.status === 401) {
            alert(error.response.data.msg);
        }
        });
        
    };

    return (
        <div className="box">
        <h1>LOGIN</h1>
            <form className="login-form" id="login-form" onSubmit={logInUser}>
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
                {loginError&&email.length<=0?
                <span className="error">Please enter an Email</span>:""}
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
                {loginError&&password.length<=0?
                <span className="error">Please enter a Password</span>:""}
            </div>
            </form>
            <div className='button-container'>
                <button className='submit-button' form="login-form">Submit</button>
            </div>
        <button className='link-button' onClick={() => {navigate('/register')}}>Don't have an account? Register here</button>
    </div>
    )
};

export default Login;