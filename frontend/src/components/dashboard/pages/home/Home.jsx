import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {getUser} from "../../../../helpers/checkUser";

const Home = (props) => {
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
            HOME
        </div>
    )
}

export default Home;