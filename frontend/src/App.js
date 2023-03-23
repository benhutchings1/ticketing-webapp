import './App.css';
import './AppMobile.css';
import React, { useState, useEffect } from "react";
import {BrowserRouter as Router, Navigate, Route, Routes, useNavigate} from "react-router-dom";
import {Landing, Login, Register} from "./components";
import {Account, EventPage, Home, QRCodeScanner, SearchPage, Shop} from "./components/dashboard/pages";
import {Navbar} from "./components/dashboard";
import {getUser, isUserLoggedIn} from "./helpers";
import {QRModal, TicketModal} from "./components/dashboard/elements";

function App() {
    // Ticket information and modal
    let [ticketOpen, setTicketOpen] = useState(false);
    const [currentEvent, setCurrentEvent] = useState({});

    // QR code information and modal
    let [qrOpen, setQROpen] = useState(false);
    let [qrData, setQRData] = useState("");

    // User array
    const [user, setUser] = useState({});

    // First we get the viewport height, and we multiply it by 1% to get a value for a vh unit
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    // We listen to the resize event
    window.addEventListener('resize', () => {
        // We execute the same script as before
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    });

    // Set user information in global variable and pass it down to routes
    useEffect(() => {
        getUser(setUser);
    }, [])

    return (
        <div className="App">
            <Router>
                <div className='pageContainer'>
                    <QRModal open={qrOpen} setOpen={setQROpen} data={qrData}/>
                    <TicketModal user={user} open={ticketOpen} setOpen={setTicketOpen} event={currentEvent}/>
                    {(isUserLoggedIn(user)) ? <Navbar user={user} /> : ""} {/* only show navbar is user exists */}
                    <div className='innerPageContainer'>
                        <Routes>
                            <Route exact path="/" element={<Landing user={user} setUser={setUser}/>}/>
                            <Route exact path="/login" element={<Login user={user} setUser={setUser}/>}/>
                            <Route exact path="/register" element={<Register user={user} setUser={setUser}/>}/>
                            <Route exact path="/home" element={<Home user={user} setUser={setUser} setCurrentEvent={setCurrentEvent}/>}/>
                            <Route exact path="/shop" element={<Shop user={user} setOpen={setTicketOpen}/>}/>
                            <Route exact path="/account" element={<Account user={user} setUser={setUser} setQRData={setQRData} setQROpen={setQROpen}/>}/>
                            <Route exact path="/event/:id" element={<EventPage user={user} event={currentEvent} setOpen={setTicketOpen} setCurrentEvent={setCurrentEvent}/>}/>
                            <Route exact path="/search" element={<SearchPage user={user} setUser={setUser} setCurrentEvent={setCurrentEvent}/>}/>

                            {/* Management Routes */}
                            <Route exact path="/scanner" element={<QRCodeScanner user={user} setUser={setUser} event={currentEvent}/>}/>

                            {/* If user tries to go to a route that doesn't exist, take them to landing page */}
                            <Route path="*" element={<Navigate to="/" />} />
                        </Routes>
                    </div>
                </div>
            </Router>
        </div>
    );
}

export default App;
