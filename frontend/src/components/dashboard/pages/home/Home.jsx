import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import './home.css';
import {getUser} from "../../../../helpers/checkUser";

const Home = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    useEffect(() => {
        if (getUser(localStorage.getItem("access_token_cookie")) != null) {
            // setUser(getUser());
        } else {
            navigate("/")
        }
    }, []);

    return (
        <div className={'contentContainer'}>
            HOME
        </div>
    )
}

export default Home;