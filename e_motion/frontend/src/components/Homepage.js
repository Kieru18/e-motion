import React, {Component} from "react";
import Login from "./Login";
import Register from "./Register";
import { BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import Dashboard from "./Dashboard";


export default class Homepage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Dashboard/>}></Route>
                <Route path="/login" element={<Login/>} />
                <Route path="/register" element={<Register/>} />
            </Routes>
        </Router>
        );

    }
}
