import React, {Component} from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "react-router-dom";
import SignInSide from "./LoginPage"; 
import SignUpSide from "./Register";

export default function Dashboard() {
   return (
        <Router>
            <Routes>
                <Route exact path="/" element={<SignInSide />}/>
                <Route path="/signup" element={<SignUpSide />} />
                <Route path="/login" element={<SignInSide />} />
            </Routes>
        </Router>
   );
}

