import './landing.css';
import './landingMobile.css';

import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom";
import {Logo} from "../../img";
import {isUserLoggedIn} from "../../helpers";

const Landing = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (isUserLoggedIn(user)) {
            navigate("/home")
        }
    }, [user])

    return (
        <div className={'landingContainer'}>
            <div className='box'>
                <img className={'landingLogo'} src={Logo}/>
                <div className={'landingButtons'}>
                    <button className='landing-button loginBtn' onClick={() => {navigate('/login')}}>LOGIN</button>
                    <button className='landing-button registerBtn' onClick={() => {navigate('/register')}}>REGISTER</button>
                </div>
            </div>
        </div>
    )
};

export default Landing;