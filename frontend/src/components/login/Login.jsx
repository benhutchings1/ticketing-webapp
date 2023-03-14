import "./login.css";

import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../helpers";
import { element } from "prop-types";

const Login = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    const [values, setValues] = useState({
        email:"",
        password:""
    })
    const [focusedEmail, setFocusedEmail] = useState(false)
    const [focusedPassword, setFocusedPassword] = useState(false)

    const errorMessage = {
        emailError: "Invalid Email",
        passwordError: "Invalid Password"
    }

    const onChange = (e) => {
        setValues({ ...values, [e.target.name]: e.target.value})
    }

    const navigate = useNavigate();

    const logInUser = async (event) => {
        event.preventDefault();
        
        const data = {
            email_address: values.email,
            password: values.password
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
                    value={values.email}
                    onChange={onChange}
                    onBlur={(e) => setFocusedEmail(true)}
                    focused={String(focusedEmail)}
                    id="email"
                    name="email"
                    placeholder="youremail@gmail.com"
                    required
                    // pattern="([-a-zA-Z0-9.`?{}]+@\w+\.\w+)" //TODO: remove when finished with testing
                />
                <span className="error">{errorMessage.emailError}</span>
            </div>
            <div className='input-container'>
                <label>Password: </label>
                <input
                    type="password"
                    value={values.password}
                    onChange={onChange}
                    onBlur={(e) => setFocusedPassword(true)}
                    focused={String(focusedPassword)}
                    id="password"
                    name="password"
                    placeholder="********"
                    required
                />
                <span className="error">{errorMessage.passwordError}</span>
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