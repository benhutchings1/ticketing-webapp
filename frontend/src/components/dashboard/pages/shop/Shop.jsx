import {useEffect, useState} from "react";
import {getUser} from "../../../../helpers/checkUser";
import {useNavigate} from "react-router-dom";

const Shop = (props) => {
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
            SHOP
        </div>
    )
}

export default Shop;