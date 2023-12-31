import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import SignInSide from "./LoginPage";
import Dashboard from "./Dashboard";
import SignUpSide from "./Register";
import LabelStudioFrontend from "./LabelStudioFrontend";

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
                <Routes>
                    <Route
                        exact path="/"
                        element={<SignInSide />}
                    />
                    <Route path="/login" element={<SignInSide />} />
                    <Route path="/signup" element={<SignUpSide />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    {/* <Route path="/label_studio" element={<LabelStudioFrontend />} /> */}
                </Routes>
            </Router>
        </div>
    );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
