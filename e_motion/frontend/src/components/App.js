import React, { Component } from 'react';
import { createRoot } from 'react-dom/client';
import Dashboard from './Dashboard';



export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Dashboard/>
        );
    }
}


const appDiv = document.getElementById("app");
const root = createRoot(appDiv);
root.render(<App />);
