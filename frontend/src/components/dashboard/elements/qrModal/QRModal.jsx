import './qrModal.css';
import './qrModalMobile.css';

import {useEffect, useState} from "react";
import QRCode from "react-qr-code";
import {Logo} from "../../../../img";
import Fireworks from 'fireworks-js';

const QRModal = (props) => {
    let open = props.open;
    let setOpen = props.setOpen;
    let data = props.data;

    const [displayStyle, setDisplayStyle] = useState("none");
    const [fireworks, setFireworks] = useState(null);

    useEffect(() => {
        if (open) {
            setDisplayStyle("flex");
        } else {
            setDisplayStyle( "none");
        }
    }, [open]);

    useEffect(() => {
        if (fireworks) {
          const timeoutId = setTimeout(() => {
            fireworks.clear();
          }, 200);
          return () => clearTimeout(timeoutId);
        }
      }, [fireworks]);
    
      useEffect(() => {
        const container = document.getElementById('fireworks-container');
        const options = {
          maxRockets: 10,
          rocketSpawnInterval: 150,
          burstRadius: 200,
          explosionPower: 15,
          color: ['#ffffff', '#ff0000', '#0000ff']
        };
        const fw = new Fireworks(container, options);
            setFireworks(fw);

            const handleClick = (event) => {
            const { clientX, clientY } = event;
            fw.fire({ x: clientX, y: clientY });
            };
            container.addEventListener('click', handleClick);

        return () => {
            container.removeEventListener('click', handleClick);
        };
  }, []);

    return (
        <div onClick={() => {setOpen(false)}} style={{display: displayStyle}} className='modalContainer noSelect'>
            <div onClick={(e) => {e.stopPropagation();}} className='modalBoxContainer'>
                <QRCode
                    size={256}
                    style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                    value={data}
                    viewBox={`0 0 256 256`}
                    onLoad={(svg) => {
                        const options = {
                          maxRockets: 10,
                          rocketSpawnInterval: 150,
                          burstRadius: 200,
                          explosionPower: 15,
                          color: ['#ffffff', '#ff0000', '#0000ff']
                        };
                        const fw = new Fireworks(svg, options);
                        setFireworks(fw);
                      }}
                />
               <img className={'qrLogoAnim'} src={Logo} />
               <div id="fireworks-container" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}></div>
            </div>
        </div>
    )
}

export default QRModal;