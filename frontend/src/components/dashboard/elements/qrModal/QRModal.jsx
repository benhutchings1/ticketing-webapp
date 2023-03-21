import './qrModal.css';
import './qrModalMobile.css';

import {useEffect, useState} from "react";
import QRCode from "react-qr-code";
import {Logo} from "../../../../img";
import {newFireWorkStar} from "./fireworks";

const QRModal = (props) => {
    let open = props.open;
    let setOpen = props.setOpen;
    let data = props.data;

    const [displayStyle, setDisplayStyle] = useState("none");

    useEffect(() => {
        if (open) {
            setDisplayStyle("flex");
        } else {
            setDisplayStyle( "none");
        }
    }, [open]);

    return (
        <div onClick={() => {setOpen(false)}} style={{display: displayStyle}} className='modalContainer noSelect'>
            <div onClick={(e) => {e.stopPropagation();}} className='modalBoxContainer'>
                <QRCode onClick={() => {newFireWorkStar(window.innerWidth / 2, window.innerHeight / 2)}}
                    size={256}
                    style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                    value={data}
                    viewBox={`0 0 256 256`}
                />
                <img className={'qrLogoAnim'} src={Logo} />
            </div>
        </div>
    )
}

export default QRModal;