import * as React from 'react';
import { useNavigate } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
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
import ProjectsTable from './ProjectsTable';
import CreateProjectDialog from './CreateProjectDialog';
import EditProjectDialog from './EditProjectDialog';
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
 * Dashboard Component
 *
 * The main dashboard component that displays projects and provides navigation.
 *
 * @component
 * @example
 * // Example usage:
 * <Dashboard />
 *
 * @returns {JSX.Element} Rendered Dashboard component.
 */
export default function Dashboard() {
  const navigate = useNavigate();
  const [projects, setProjects] = React.useState([]);
  const [shouldListProjects, setShouldListProjects] = React.useState(false);
  const [selectedProject, setSelectedProject] = React.useState({});
  const [openEditDialog, setOpenEditDialog] = React.useState(false);
  const { enqueueSnackbar } = useSnackbar();
 
  // Function to fetch projects
  const fetchProjects = () => {
    fetch("/api/list_projects", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then((response) => {
      if (!response.ok) {
        console.log("Error");
      }
      return response.json();
    })
    .then((data) => setProjects(data))
    .catch((error) => console.log(error));
  };

  // fetch projects when Dashboard is mounted
  React.useEffect(() => {
    fetchProjects();
  }, []);

  // fetch projects after dialog is closed
  React.useEffect(() => {
    if (shouldListProjects) {
      fetchProjects();
      setShouldListProjects(false);
    }
  }, [shouldListProjects]);

  const handleRowClick = (row) => {
    setSelectedProject(row);
    setOpenEditDialog(true);
  };

  const handleCloseEditDialog = () => {
    setSelectedProject(null);
    setShouldListProjects(true);
    setOpenEditDialog(false);
  };

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

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <MuiAppBar position="absolute" >
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
              Dashboard
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
                  <ProjectsTable data={projects} onChange={handleRowClick}/>
                </Paper>
                <CreateProjectDialog onClose={setShouldListProjects}/>
                {openEditDialog && (
                  <EditProjectDialog
                    open={openEditDialog}
                    row={selectedProject}
                    onClose={handleCloseEditDialog}
                  />
                )}
              </Grid>
            </Grid>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
