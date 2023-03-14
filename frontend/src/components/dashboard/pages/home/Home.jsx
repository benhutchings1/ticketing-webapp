import './home.css';
import Ticket from '../../elements/ticket/Ticket';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";

const Home = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])


}

export default Home;