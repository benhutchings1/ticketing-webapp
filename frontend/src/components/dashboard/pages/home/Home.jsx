import './home.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";

const Home = (props) => {
    const user = props.user;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    return (
        <div className={'contentContainer'}>
            <h1 className={'dashboardTitle'}>HOME</h1>
            {user != null && user.role !== "management" ?
                // User page
                <div>

                </div>
            :
                // Management page
                <div>
                    <button className={'qrCodeBtn'} onClick={() => {navigate("/scanner")}}>SCAN QR CODE</button>
                </div>}
        </div>
    )
}

export default Home;