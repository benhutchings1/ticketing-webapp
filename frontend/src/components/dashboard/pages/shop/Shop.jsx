import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {SearchBar} from "../../elements";

const Shop = (props) => {
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
            <SearchBar/>
            <h1 className={'dashboardTitle'}>SHOP</h1>
        </div>
    )
}

export default Shop;