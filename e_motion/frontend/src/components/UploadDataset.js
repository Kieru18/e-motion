import * as React from 'react';
import { useNavigate } from "react-router-dom";
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import { TextField } from '@mui/material';
import Badge from '@mui/material/Badge';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import { mainListItems } from './listItems';
import { useLocation } from "react-router-dom";
import { useState } from 'react';
import Input from '@mui/material/Input';
import Stack from '@mui/material/Stack';



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

export default function UploadDataset() {
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = React.useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [success, setSuccess] = React.useState(false)
  

  const toggleDrawer = () => {
    setOpen(!open);
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    setSelectedFiles([...selectedFiles, ...files]);
  };

  const handleRemoveFile = (index) => {
    const newFiles = [...selectedFiles];
    newFiles.splice(index, 1);
    setSelectedFiles(newFiles);
  };

  const handleUpload = async () => {
    setError(false)
    setSuccess(false)
    
    const formData = new FormData();
    const projectId = location.state.project_id;
    const apiUrl = `/api/upload/${projectId}/`;

    selectedFiles.forEach((file) => {
      formData.append('files[]', file);
    });

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
          },
        body: formData,
      });
  
      if (response.ok) {
        console.log('Files uploaded successfully');
        const success = await response.json();
        setSuccess(success)
        
      } else {
        console.error('File upload failed');
        const error = await response.json();
        setError(error.error);
        return;
      }
    } catch (error) {
        console.error('Error during file upload:', error);
        setError('An unexpected error occurred during file upload.');
    }
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
              Upload Dataset for the project {location.state.project_title}, id: {location.state.project_id}
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
            <List>
                <Input
                type="file"
                inputProps={{ multiple: true }}
                onChange={handleFileChange}
                />
                <Stack spacing={1}>
                    {selectedFiles.map((file, index) => (
                    <div key={index}>
                        {file.name}
                        <Button size="small" onClick={() => handleRemoveFile(index)}>
                        Remove
                        </Button>
                    </div>
                    ))}
                </Stack>
                {error && (
                    <Typography variant="body2" color="error" align="center">
                    {error}
                    </Typography>
                )}
                {success && (
                    <Typography variant="body2" color="success.main" align="center">
                    There were {success.files_count} images uploaded successfully.
                    </Typography>
                )}
            <ListItem>
                <Button variant="contained" onClick={handleUpload}>
                    Upload
                </Button>
            </ListItem>
            
            </List>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
