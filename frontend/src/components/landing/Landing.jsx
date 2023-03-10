import React, {useEffect, useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../helpers/checkUser";
import './landing.css';
import './landingMobile.css';

const Landing = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    const logoutUser = async () => {
        await httpClient.post("//localhost:5000/logout");
        navigate("/")
    };

    useEffect(() => {
        if (getUser() != null) {
            setUser(getUser());
        } else {
            navigate("/")
        }
    }, []);

    return (
        <div className={'landingPage'}>
            <h1>Ticketing App</h1>
            {user != null ? (
                <div>
                    <h2>Logged in</h2>
                    <h3>ID: {user.id}</h3>
                    <h3>Email: {user.email}</h3>

                    <button onClick={logoutUser}>Logout</button>
                </div>
            ) : (
                <div>
                    {/*<p>You are not logged in</p>*/}
                    <div className={'landingButtons'}>
                        <button onClick={() => {navigate('/login')}}>Login</button>
                        <button onClick={() => {navigate('/register')}}>Register</button>
                    </div>
                </div>
            )}
            <div className={'gradient'}></div>
        </div>
    )
};

export default Landing;