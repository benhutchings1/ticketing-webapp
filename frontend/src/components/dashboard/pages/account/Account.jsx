import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../../../helpers/checkUser";

const Account = (props) => {
    const [user, setUser] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        if (getUser() != null) {
            setUser(getUser());
        } else {
            navigate("/")
        }
    }, []);

    return (
        <div>
            ACCOUNT
        </div>
    )
}

export default Account;