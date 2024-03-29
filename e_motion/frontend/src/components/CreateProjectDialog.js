import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import ListItemText from '@mui/material/ListItemText';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import TextField from '@mui/material/TextField';
import { useSnackbar } from 'notistack';

/**
 * Transition component for the dialog slide effect.
 * @param {Object} props - Component properties.
 * @param {Object} ref - Forwarded ref.
 * @returns {JSX.Element} Slide component.
 */
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

/**
 * CreateProjectDialog Component
 *
 * A dialog component for creating a new project with title, description, and dataset URL.
 *
 * @component
 * @example
 * // Example usage:
 * <CreateProjectDialog onClose={(success) => console.log(`Project creation ${success ? 'succeeded' : 'failed'}`)} />
 *
 * @param {Object} props - The properties of the component.
 * @param {function} props.onClose - Callback function called when the dialog is closed.
 * @returns {JSX.Element} Rendered CreateProjectDialog component.
 */
export default function CreateProjectDialog(props) {
  const [open, setOpen] = React.useState(false);
  const [error, setError] = React.useState(false);
  const [title, setTitle] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [label_studio_project, setLabelStudioProject] = React.useState("");
  const { enqueueSnackbar } = useSnackbar();

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSave = async (event) => {
    event.preventDefault();

    if (!title || !description || !label_studio_project) {
      enqueueSnackbar('Please fill out all fields', { variant: 'error' });
      return;
    }

    try {
      const response = await fetch('/api/create_project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
        },
        body: JSON.stringify({
          title,
          description,
          label_studio_project,
        }),
      });

      if (!response.ok) {
        enqueueSnackbar('Project creation failed', { variant: 'error' });
        const error = await response.json();
        setError(error.detail);
        return;
      }

      enqueueSnackbar('Project created successfully', { variant: 'success' });
      setOpen(false);
      props.onClose(true);
    } catch (error) {
      console.error('Error', error);
    }
  };

  return (
    <React.Fragment>
      <Button variant="outlined" onClick={handleClickOpen}>
        Create Project
      </Button>
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              New Project
            </Typography>
            <Button autoFocus color="inherit" onClick={handleSave}>
              save
            </Button>
          </Toolbar>
        </AppBar>
        <List>
          <ListItem>
            <TextField
              required
              fullWidth
              label="Title"
              id="fullWidth"
              onChange={(event) => setTitle(event.target.value)}
            />
          </ListItem>
          <Divider />
          <ListItem>
            <TextField
              required
              fullWidth
              id="outlined-multiline-static"
              label="Description"
              multiline
              rows={4}
              onChange={(event) => setDescription(event.target.value)}
            />
          </ListItem>
          <Divider />
          <ListItem>
            <TextField
              required
              fullWidth
              label="Label Studio Project ID"
              id="fullWidth"
              onChange={(event) => setLabelStudioProject(event.target.value)}
            />
          </ListItem>
          {error && (
            <Typography variant="body2" color="error" align="center">
              {error}
            </Typography>
          )}
        </List>
      </Dialog>
    </React.Fragment>
  );
}
