import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import './home.css';

const Home = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    useEffect(() => {
        setUser([]) // for testing purposes
        // if (getUser() != null) {
        //     setUser(getUser());
        // } else {
        //     navigate("/")
        // }
    }, []);

    return (
        <div>
            HOME
        </div>
    )
}

export default Home;