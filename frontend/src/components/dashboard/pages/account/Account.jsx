import './account.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

const Account = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    const [firstLetter, setFirstLetter] = useState("")

    const navigate = useNavigate();

    // Generate random colour on first visit
    useEffect(() => {
        let randomColour = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
        document.getElementById('accountPicture').style.backgroundColor = randomColour;
    }, [])

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        } else if (user.firstname != null) {
            setFirstLetter(user.firstname[0])
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
            <h1 className={'dashboardTitle'}>ACCOUNT</h1>
            {(user != null) ?
                <div>
                    <div className={'accountDetails'}>
                        <div id={'accountPicture'} className={'accountPicture'}>
                            {firstLetter}
                        </div>
                        <br/>
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
                    <br/>
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