import './App.css';
import './AppMobile.css';
import React, { useState, useEffect } from "react";
import {BrowserRouter as Router, Navigate, Route, Routes, useNavigate} from "react-router-dom";
import {Landing, Login, Register} from "./components";
import {Account, EventPage, Home, QRCodeScanner, SearchPage, Shop} from "./components/dashboard/pages";
import {Navbar} from "./components/dashboard";
import {getUser, isUserLoggedIn} from "./helpers";
import {TicketModal} from "./components/dashboard/elements";

function App() {
    // For ticket modal
    let [open, setOpen] = useState(false);

    const [user, setUser] = useState({});
    const [currentEvent, setCurrentEvent] = useState({});

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

    useEffect(() => {
        getUser(setUser);
    }, [])

    return (
        <div className="App">
            <Router>
                <div className='pageContainer'>
                    <TicketModal user={user} open={open} setOpen={setOpen} event={currentEvent}/>
                    {(isUserLoggedIn(user)) ? <Navbar user={user} /> : ""} {/* only show navbar is user exists */}
                    <div className='innerPageContainer'>
                        <Routes>
                            <Route exact path="/" element={<Landing user={user} setUser={setUser}/>}/>
                            <Route exact path="/login" element={<Login user={user} setUser={setUser}/>}/>
                            <Route exact path="/register" element={<Register user={user} setUser={setUser}/>}/>
                            <Route exact path="/home" element={<Home user={user} setCurrentEvent={setCurrentEvent}/>}/>
                            <Route exact path="/shop" element={<Shop user={user}/>}/>
                            <Route exact path="/account" element={<Account user={user} setUser={setUser}/>}/>
                            <Route exact path="/event/:id" element={<EventPage user={user} event={currentEvent} setOpen={setOpen}/>}/>
                            <Route exact path="/search" element={<SearchPage user={user} setCurrentEvent={setCurrentEvent}/>}/>

                            {/* Management Routes */}
                            <Route exact path="/scanner" element={<QRCodeScanner user={user} setUser={setUser}/>}/>

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
