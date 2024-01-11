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
import CreateModelDialog from './CreateModelDialog';
import DeleteProjectDialog from './DeleteProjectDialog';
import { useNavigate } from "react-router-dom";
import UploadDatasetDialog from './UploadDatasetDialog';
import { useSnackbar } from "notistack";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function EditProjectDialog(props) {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(true);
  const [error, setError] = React.useState(false);
  const [id, setId] = React.useState(null);
  const [title, setTitle] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [dataset_url, setUrl] = React.useState("");
  const { enqueueSnackbar } = useSnackbar();

  React.useEffect(() => {
    if (open && props.row) {
      setId(props.row.id);
      setTitle(props.row.title);
      setDescription(props.row.description);
      setUrl(props.row.dataset_url);
    }
  }, [open, props.row]);

  const handleClose = () => {
    setOpen(false);
    props.onClose();
  };

  const handleSave = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('/api/edit_project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
        },
        body: JSON.stringify({
          id,
          title,
          description,
          dataset_url,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        setError(error.detail);
        return;
      }
      handleClose();
    } catch (error) {
      console.error('Error', error);
    }
    handleClose();
  };

  const handleOpenLS = () => {
    // TODO: set Label Studio Docker link: (http://localhost:8089/user/login/)
    window.open('https://www.google.com/', '_blank', 'noreferrer');
  };

  const handleMakePredictions = () => {
    navigate('/predict', { state: { project_id: id } })
  };

  return (
    <React.Fragment>
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
              Project Overview
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
              defaultValue={title}
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
              defaultValue={description}
              onChange={(event) => setDescription(event.target.value)}
            />
          </ListItem>
          <Divider />
          <ListItem>
            <TextField
              required
              fullWidth
              label="Dataset URL"
              id="fullWidth"
              defaultValue={dataset_url}
              onChange={(event) => setUrl(event.target.value)}
            />
          </ListItem>
          {error && (
            <Typography variant="body2" color="error" align="center">
              {error}
            </Typography>
          )}
          <Divider />
          <DeleteProjectDialog projectId={id} close={handleClose}/>
          <UploadDatasetDialog projectId={id} projectTitle={title} />
          <Button variant="outlined" onClick={handleOpenLS}>
            Go to Manual Annotation
          </Button>
          <CreateModelDialog projectId={id} projectTitle={title}/>
          <Button variant="outlined" onClick={handleMakePredictions}>
            Go to Make Predictions
          </Button>
        </List>
      </Dialog>
    </React.Fragment>
  );
}
