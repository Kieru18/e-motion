import React, { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from "react-router-dom";
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

const handleRedirectToLogin = () => {
    navigate('/login');
  }

  /**
 * Sign Up Page Component
 *
 * The component responsible for rendering the sign-up page. Allows users to register
 * by providing a username, email, and password.
 *
 * @component
 * @example
 * // Example usage:
 * <SignUpSide />
 *
 * @returns {JSX.Element} Rendered Sign Up Page component.
 */
export default function SignUpSide() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [email, setEmail] = useState('');
  const { enqueueSnackbar } = useSnackbar();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('')

    if (!username || !email || !password) {
      enqueueSnackbar('Please fill out all required fields', { variant: 'error' });
      return;
    }

    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          email,
        }),
      });

      if (!response.ok) {
        // Handle error cases
        const error = await response.json();
        const errorMessage = error.username || error.email || Array('Registration failed');
        setError(errorMessage);
        enqueueSnackbar(errorMessage[0], { variant: 'error' });
        console.log(error)
        return;
      }

      const data = await response.json();
      // Handle successful registration
      localStorage.setItem('token', data.token);  // LOCALSTORAGE
      console.log('Registration successful', data);
      enqueueSnackbar('Registration successful', { variant: 'success' });
      navigate('/dashboard');
    } catch (error) {
      console.error('Error during registration', error);
      enqueueSnackbar('Error during registration', { variant: 'error' });
    }
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Grid container component="main" sx={{ height: '100vh' }}>
        <CssBaseline />
        <Grid
          item
          xs={false}
          sm={4}
          md={7}
          sx={{
            backgroundRepeat: 'no-repeat',
            backgroundColor: (t) =>
              t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <Box
            sx={{
              my: 8,
              mx: 4,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="email"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>

              {error && (
                <Typography variant="body2" color="error" align="center">
                {error}
                </Typography>
              )}
              <Grid container>
                <Grid item>
                  <Link href="/login" variant="body2" onClick={handleRedirectToLogin}>
                    Already have an account? Sign In
                  </Link>
                </Grid>
              </Grid>
              <Copyright sx={{ mt: 5 }} />
            </Box>
          </Box>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}