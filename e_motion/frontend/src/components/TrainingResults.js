import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import Container from "@mui/material/Container";
import { AppBar, Grid, Toolbar } from "@mui/material";
import Scores from "./Scores";

import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme();

export default function TrainingResultsPage(props) {
  const navigate = useNavigate();
  const location = useLocation();

  // const metrics = {
  //   miou: location.state["miou"],
  //   top1: location.state["top1"],
  //   top5: location.state["top5"],
  // };

  const metrics = {
    miou: 0.56,
    top1: 0.66,
    top5: 0.76,
  };

  const handlePredictionsClick = () => {
    navigate('/predict'); // , { state: { project_id: location.state.project_id } }
  };

  const handleDashboardClick = () => {
    navigate('/dashboard');
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar position="absolute">
          <Toolbar
            sx={{
              pr: "24px", // keep right padding when drawer closed
            }}
          >
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Training results
            </Typography>
            <Button
              variant="contained"
              sx={{ my: 1, mx: 1.5 }}
            //   onClick={handleLogout}
            >
              Logout
            </Button>
          </Toolbar>
        </AppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Scores data={metrics} sx={{ width: '80%' }} />

            <Grid container spacing={2} justifyContent="center" sx={{ mt: 2 }}>
              <Grid item>
                <Button variant="contained" onClick={handlePredictionsClick}>Go to Make predictions</Button>
              </Grid>
              <Grid item>
                <Button variant="contained" onClick={handleDashboardClick}>Back to Dashboard</Button>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}