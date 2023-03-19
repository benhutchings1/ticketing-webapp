import './qrCodeScanner.css';
import './qrCodeScannerMobile.css';

import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {QrScanner} from '@yudiel/react-qr-scanner';
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

const QRCodeScanner = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    let event = props.event;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null || (user != null && user.role !== "management")) {
            navigate("/")
        }
    }, [user])

    return (
        <div className={'contentContainer qrScannerDiv'}>
            <QrScanner
                onDecode={(result) => {
                    console.log(result)
                    const data = {
                        event_id: event.event_id,
                        qr_data: result
                    }

                    httpClient.post('/ticket/validate', data, {
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRF-TOKEN": getCookie("csrf_access_token"),
                        }
                    })
                    .then(response => {
                        console.log(response)
                        alert("valid")
                    })
                    .catch(error => {
                        console.log(error)
                        if (error.response && error.response.status === 400) {
                            alert("invalid")
                            // invalid ticket
                        }
                    });
                }}
                onError={(error) => console.log(error?.message)}
            />
        </div>
    )
}

export default QRCodeScanner;