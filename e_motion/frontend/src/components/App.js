import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import SignInSide from "./LoginPage";
import Dashboard from "./Dashboard";
import SignUpSide from "./Register";
import TrainingResultsPage from "./TrainingResults";
import MakePredictionsPage from "./MakePredictions";
import LabelStudioFrontend from "./LabelStudioFrontend";
import { SnackbarProvider } from "notistack";
import Slide from "@mui/material/Slide";

import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "react-router-dom";

function SlideTransition(props) {
    return <Slide {...props} direction="up" />;
}


export default function App(props) {
    return (
        <SnackbarProvider maxSnack={3} 
                          TransitionComponent={SlideTransition}
                          sx={{
                            '& .MuiSnackbarContent-root': {
                                '&.MuiSnackbarContent-message': {
                                    border: '1px solid #4caf50',
                                },
                                '&.MuiSnackbarContent-message.Mui-error': {
                                    border: '1px solid #f44336',
                                },
                                '&.MuiSnackbarContent-message.Mui-info': {
                                    border: '1px solid #2196f3',
                                },
                            },
                        }}
        >
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
                        <Route path="/results" element={<TrainingResultsPage />} />
                        <Route path="/predict" element={<MakePredictionsPage />} />
                    </Routes>
                </Router>
            </div>
        </SnackbarProvider>
    );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
