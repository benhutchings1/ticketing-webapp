import './account.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

const Account = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    const logoutUser = async () => {
        httpClient.post('/logout', {}, {
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": getCookie("csrf_access_token"),
            }
        })
        .then(response => {
            console.log(response)
            setUser(null)
            navigate("/");
        })
        .catch(error => {
            console.log(error.response.data);
            if (error.response && error.response.status === 401) {
                alert(error.response.data.msg);
            }
        });
    };

    return (
        <div className={'contentContainer'}>
            <h1>ACCOUNT</h1>
            {(user != null) ?
                <div>
                    <div className={'accountDetails'}>
                        <b>Email:</b>{user.email}
                        <br/><br/>
                        <b>Name:</b>
                        {`${user.firstname} ${user.surname}`}
                        <br/><br/>
                        <b>Date of Birth:</b>
                        {user.date_of_birth}
                        <br/><br/>
                        <b>Postcode:</b>
                        {user.postcode}
                        <br/><br/>
                        <b>Phone Number:</b>
                        {user.phone_number}
                    </div>
                    <br/><br/>
                    <button className={'logoutBtn'} onClick={() => logoutUser()}>
                        LOGOUT
                    </button>
                </div>
            :
                <div></div>
            }
        </div>
    )
}

export default Account;