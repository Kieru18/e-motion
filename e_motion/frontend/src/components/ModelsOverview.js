import * as React from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import ModelsTable from './ModelsTable';
import { useSnackbar } from 'notistack';

/**
 * Copyright component for displaying copyright information.
 *
 * @param {Object} props - The properties of the component.
 * @returns {JSX.Element} Rendered Copyright component.
 */
function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit">
        E-motion
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

/**
 * ModelsOverviewPage Component
 *
 * A page component for displaying a list of models associated with a project.
 *
 * @component
 * @example
 * // Example usage:
 * <ModelsOverviewPage />
 *
 * @returns {JSX.Element} Rendered ModelsOverviewPage component.
 */
export default function ModelsOverviewPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = React.useState(true);
  const [project_id, setProject_Id] = React.useState(location.state.project_id);
  const [project_name, setProjectName] = React.useState(location.state.project_name);
  const [models, setModels] = React.useState([]);
  const [selected_id, setSelected_Id] = React.useState(0);
  const { enqueueSnackbar } = useSnackbar();

  const fetchModels = () => {
    fetch(`/api/list_models/${project_id}/`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch models");
      }
      return response.json();
    })
    .then((data) => {
      if (data.length === 0) {
        navigate('/dashboard'); // Redirect to '/dashboard' if models array is empty
      } else {
        setModels(data);
      }
    })
    .catch((error) => console.log(error));
  };

  // fetch models when component is mounted
  React.useEffect(() => {
    fetchModels();
  }, []);

  const handleLogout = () => {
    const requestOptions = {
      method: "GET",
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
      },
    };
    fetch("/api/logout", requestOptions).then(() => {
      navigate("/");
      enqueueSnackbar('You have been logged out', { variant: 'info' });
      localStorage.removeItem('token');  // LOCALSTORAGE
    });
  };

  const handleMakePrecition = () => {
    fetch(`/api/make_predictions/${project_id}/${selected_id}/`, {
      method: "GET",
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then(response => {
      if (response.ok) {
          return response.blob();
      } else {
          console.error('File download failed.');
          enqueueSnackbar('File download failed.', { variant: 'error' });
      }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `annotations.json`;
        document.body.appendChild(link);
        link.click();
        // Cleanup
        window.URL.revokeObjectURL(url);
        enqueueSnackbar('Prediciton successful', { variant: 'success' });
    })
    .catch(error => {
        console.error('Error:', error);
        enqueueSnackbar(error, { variant: 'error' });
        
    });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <MuiAppBar position="absolute" open={open}>
          <Toolbar
            sx={{
              pr: '24px',
            }}
          >
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Models List
            </Typography>
            <Button
              variant="contained"
              sx={{ my: 1, mx: 1.5 }}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Toolbar>
        </MuiAppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <ModelsTable data={models} project_name={project_name} onSelect={setSelected_Id} />
                </Paper>
              </Grid>
            </Grid>
            <Button
                variant="contained"
                onClick={handleMakePrecition}
              >
                Predict
              </Button>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
