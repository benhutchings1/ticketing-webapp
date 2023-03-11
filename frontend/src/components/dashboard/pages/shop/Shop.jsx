import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";

const Shop = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    return (
        <div className={'contentContainer'}>
            <h1>SHOP</h1>
        </div>
    )
}

export default Shop;