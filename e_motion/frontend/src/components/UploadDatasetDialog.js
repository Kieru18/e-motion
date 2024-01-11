import * as React from 'react';
import { useNavigate } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import AppBar from '@mui/material/AppBar';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import { useState } from 'react';
import Input from '@mui/material/Input';
import Stack from '@mui/material/Stack';
import Dialog from '@mui/material/Dialog';
import { useSnackbar } from 'notistack';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const defaultTheme = createTheme();

export default function UploadDatasetDialog(props) {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const projectId = props.projectId;
  const projectTitle = props.projectTitle;
  const { enqueueSnackbar } = useSnackbar();


  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
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

    const formData = new FormData();
    const apiUrl = `/api/upload/${projectId}/`;

    selectedFiles.forEach((file) => {
      formData.append('files[]', file);
    });

    if (!selectedFiles) {
      enqueueSnackbar('Please select files', { variant: 'error' });
      return;
    }


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
        enqueueSnackbar('All files uploaded successfully', { variant: 'success' });
        return;
        
      } else {
        console.error('File upload failed');
        const error = await response.json();
        enqueueSnackbar(error.error, { variant: 'error' });
        return;
      }
    } catch (error) {
        console.error('Error during file upload', error);
        enqueueSnackbar('Files upload failed', { variant: 'error' });
        return;
    }
  };

  return (
    <React.Fragment>
      <Button variant="outlined" onClick={handleClickOpen}>
          Upload Dataset
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
                    Upload dataset for Project {projectTitle} (id: {projectId})
                </Typography>
                <Button autoFocus color="inherit" onClick={handleUpload}>
                    Upload
                </Button>
            </Toolbar>
        </AppBar>
        
          <List>
            <ListItem>
            <Input
              type="file"
              inputProps={{ multiple: true }}
              fullWidth
              onChange={handleFileChange}
            />
            </ListItem>
            <ListItem>
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
            </ListItem>
            </List>
        </Dialog>
    </React.Fragment>
  );
}
