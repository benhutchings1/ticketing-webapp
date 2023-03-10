import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../../../helpers/checkUser";

const Account = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    useEffect(() => {
        if (getUser() != null) {
            getUser().then(r => {
                setUser(r);
            })
        } else {
            navigate("/")
        }
    }, []);

    return (
        <div className={'contentContainer'}>
            ACCOUNT
            <div>
                {user.email}
            </div>
        </div>
    )
}

export default Account;