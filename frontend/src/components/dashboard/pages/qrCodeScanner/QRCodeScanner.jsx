import './qrCodeScanner.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {QrScanner} from '@yudiel/react-qr-scanner';

const QRCodeScanner = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null || (user != null && user.role !== "management")) {
            navigate("/")
        }
    }, [user])

    return (
        <div className={'contentContainer'}>
            <QrScanner
                onDecode={(result) => alert(result)}
                onError={(error) => console.log(error?.message)}
            />
        </div>
    )
}

export default QRCodeScanner;