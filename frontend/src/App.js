import './App.css';
import React, { useState, useEffect } from "react";
import {BrowserRouter as Router, Navigate, Route, Routes} from "react-router-dom";
import {Home, Login, Register} from "./components";

function App() {
  return (
    <div className="App">
      <Router>
        <div>
          <Routes>
            <Route exact path="/" element={<Home/>}/>
            <Route exact path="/login" element={<Login/>}/>
            <Route exact path="/register" element={<Register/>}/>
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
