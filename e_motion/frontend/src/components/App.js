import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import SignInSide from "./LoginPage";
import Dashboard from "./Dashboard";
import SignUpSide from "./Register";
import PrivateRoute from "./utils/PrivateRoute"
import AuthProvider from "../context/AuthContext";

import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "react-router-dom";

export default function App(props) {
    return (
        <div className="center">
            <Router>
                <AuthProvider>
                <Routes>
                    <PrivateRoute exact path="/"  component={Dashboard} />   
                    <Route path="/login" element={<SignInSide />} />
                    <Route path="/signup" element={<SignUpSide />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
                </AuthProvider>
            </Router>
        </div>
    );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
