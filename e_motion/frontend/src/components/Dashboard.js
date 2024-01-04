import * as React from 'react';
import { useNavigate } from "react-router-dom";
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { mainListItems } from './listItems';
import ProjectsTable from './ProjectsTable';
import CreateProjectDialog from './CreateProjectDialog';
import EditProjectDialog from './EditProjectDialog';


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

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

const defaultTheme = createTheme();

export default function Dashboard() {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(true);
  const [projects, setProjects] = React.useState([]);
  const [shouldListProjects, setShouldListProjects] = React.useState(false);
  const [selectedProject, setSelectedProject] = React.useState({});
  const [openEditDialog, setOpenEditDialog] = React.useState(false);

  const toggleDrawer = () => {
    setOpen(!open);
  };

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
        console.log("PROBLEM");
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
      localStorage.removeItem('token');  // LOCALSTORAGE
    });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar position="absolute" open={open}>
          <Toolbar
            sx={{
              pr: '24px', // keep right padding when drawer closed
            }}
          >
            <IconButton
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={toggleDrawer}
              sx={{
                marginRight: '36px',
                ...(open && { display: 'none' }),
              }}
            >
              <MenuIcon />
            </IconButton>
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
        </AppBar>
        <Drawer variant="permanent" open={open}>
          <Toolbar
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              px: [1],
            }}
          >
            <IconButton onClick={toggleDrawer}>
              <ChevronLeftIcon />
            </IconButton>
          </Toolbar>
          <Divider />
          <List component="nav">
            {mainListItems}
            <Divider sx={{ my: 1 }} />
          </List>
        </Drawer>
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
