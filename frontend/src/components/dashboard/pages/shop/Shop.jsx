import {useEffect, useState} from "react";
import {getUser} from "../../../../helpers/checkUser";
import {useNavigate} from "react-router-dom";

const Shop = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    useEffect(() => {
        if (getUser() != null) {
            setUser(getUser());
        } else {
            navigate("/")
        }
    }, []);

    return (
        <div className={'contentContainer'}>
            SHOP
        </div>
    )
}

export default Shop;