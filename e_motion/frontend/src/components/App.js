import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import SignInSide from "./LoginPage";


export default function App(props) {
    return (
        <div className="center">
            <SignInSide />
        </div>
    );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
