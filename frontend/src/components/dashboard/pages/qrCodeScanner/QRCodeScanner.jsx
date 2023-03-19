import './qrCodeScanner.css';
import './qrCodeScannerMobile.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {QrScanner} from '@yudiel/react-qr-scanner';
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

import {Tick, Cross} from "../../../../img";

const QRCodeScanner = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    let event = props.event;
    let [validImg, setValidImg] = useState();

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
                scanDelay={7500}
                onDecode={(result) => {
                    console.log(result)
                    const data = {
                        event_id: event.event_id,
                        qr_data: result
                    }

                    httpClient.post(`${process.env.REACT_APP_ROUTE_URL}/ticket/validate`, data, {
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRF-TOKEN": getCookie("csrf_access_token"),
                        }
                    })
                    .then(response => {
                        // valid ticket
                        setValidImg(Tick);
                        setTimeout(() => {
                            setValidImg(undefined);
                        }, 3000);
                    })
                    .catch(error => {
                        console.log(error)
                        if (error.response && error.response.status === 400) {
                            // invalid ticket
                            setValidImg(Cross);
                            setTimeout(() => {
                                setValidImg(undefined);
                            }, 3000);
                        }
                    });
                }}
                onError={(error) => console.log(error?.message)}
            />

            <img className={'validImg'} src={validImg} />
            <div></div>
        </div>
    )
}

export default QRCodeScanner;