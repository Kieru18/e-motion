import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import Dasboard from "./Dashboard";
import SignInSide from "./LoginPage";


export default function App(props) {
    return (
        <div className="center">
            <Dasboard />
        </div>
    );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
