import './landing.css';
import './landingMobile.css';

import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom";

const Landing = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user != null) {
            navigate("/home")
        }
    }, [user])

    return (
        <div className='box'>
            <h1 className='welcome'>TICKETING APP</h1>
            <div>
                <div className={'landingButtons'}>
                    <button className='landing-button' onClick={() => {navigate('/login')}}>LOGIN</button>
                    <button className='landing-button' onClick={() => {navigate('/register')}}>REGISTER</button>
                </div>
            </div>
        </div>
    )
};

export default Landing;