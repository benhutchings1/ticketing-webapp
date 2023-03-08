import './App.css';
import React, { useState, useEffect } from "react";
import {BrowserRouter as Router, Navigate, Route, Routes} from "react-router-dom";
import {Landing, Login, Register} from "./components";
import {Account, Home, Shop} from "./components/dashboard/pages";

function App() {
    const [user, setUser] = useState(null);

    return (
        <div className="App">
            <Router>
                <div>
                    {/* Navbar goes here */}
                    <div>
                        <Routes>
                            <Route exact path="/" element={<Landing/>}/>
                            <Route exact path="/login" element={<Login/>}/>
                            <Route exact path="/register" element={<Register/>}/>
                            <Route exact path="/home" element={<Home/>}/>
                            <Route exact path="/shop" element={<Shop/>}/>
                            <Route exact path="/account" element={<Account/>}/>

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
