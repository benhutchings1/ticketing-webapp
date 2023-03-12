import React, {useEffect, useState} from 'react';
import './navbar.css';
import './navbarMobile.css';
import { useNavigate, useLocation } from "react-router-dom";
import {AccountIcon, HomeIcon, ShopIcon} from "../../../img";
import {detectMobile} from "../../../helpers/detectMobile";

const Navbar = (props) => {
    const user = props.user;

    const navigate = useNavigate();
    const location = useLocation();

    const [isHover, setIsHover] = useState(false);

    const styles = {
        imgStyle: {
            filter: isHover ? 'invert(0%) sepia(2%) saturate(0%) hue-rotate(69deg) brightness(100%) contrast(92%)' : 'invert(50%) sepia(100%) saturate(0%) hue-rotate(280deg) brightness(100%) contrast(75%)',
            transition: '0.2s',
        },
        selectedStyle: {
            filter: isHover ? 'invert(50%) sepia(100%) saturate(0%) hue-rotate(280deg) brightness(100%) contrast(75%)' : 'invert(0%) sepia(2%) saturate(0%) hue-rotate(69deg) brightness(100%) contrast(92%)',
            transition: '0.2s',
        }
    };

    const [homeNavColour, setHomeNavColour] = useState(false)
    const [shopNavColour, setShopNavColour] = useState(false)
    const [accountNavColour, setAccountNavColour] = useState(false)

    useEffect(() => {
        const current = location.pathname;

        if (current === `/home`) {
            setHomeNavColour(true);
        } else if (current === `/shop`) {
            setShopNavColour(true);
        } else if (current === `/account`) {
            setAccountNavColour(true);
        }
    }, [location, styles]);

    return (
        <div className='navbar'>
            <div className='navbarLinks'>
                <div className='navbarContainer'>
                    <div className="tooltip">
                        <img
                            style={homeNavColour ? styles.selectedStyle : styles.imgStyle}
                            onMouseEnter={() => setHomeNavColour(true)}
                            onMouseLeave={() => setHomeNavColour(false)}
                            onClick={() => {
                                navigate('/home')
                                setShopNavColour(false)
                                setAccountNavColour(false)
                            }}
                            src={HomeIcon}
                            alt='Home'
                        />
                        {detectMobile() ? "" : <span className="tooltipText">Home</span>}
                    </div>

                    {user !== null && user.role !== "management" ?
                        <div className="tooltip">
                            <img
                                style={shopNavColour ? styles.selectedStyle : styles.imgStyle}
                                onMouseEnter={() => setShopNavColour(true)}
                                onMouseLeave={() => setShopNavColour(false)}
                                onClick={() => {
                                    navigate('/shop')
                                    setHomeNavColour(false)
                                    setAccountNavColour(false)
                                }}
                                src={ShopIcon}
                                alt={'Shop'}
                            />
                            {detectMobile() ? "" : <span className="tooltipText">Shop</span>}
                        </div>
                    :
                        <div style={{display: "none"}}></div>
                    }

                    <div className="tooltip">
                        <img
                            style={accountNavColour ? styles.selectedStyle : styles.imgStyle}
                            onMouseEnter={() => setAccountNavColour(true)}
                            onMouseLeave={() => setAccountNavColour(false)}
                            onClick={() => {
                                navigate('/account');
                                setHomeNavColour(false)
                                setShopNavColour(false)
                            }}
                            src={AccountIcon}
                            alt='Account'
                        />
                        {detectMobile() ? "" : <span className="tooltipText">Account</span>}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Navbar