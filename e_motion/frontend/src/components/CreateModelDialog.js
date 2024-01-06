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
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';


const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

export default function CreateModelDialog(props) {
    const [open, setOpen] = React.useState(false);
    const [error, setError] = React.useState(false);
    const [name, setName] = React.useState("");
    const [architecture, setArchitecture] = React.useState("");
    const [learning_rate, setLearningRate] = React.useState("");
    const [weight_decay, setWeightDecay] = React.useState("");
    const [epochs, setEpochs] = React.useState("");
    const [validation_set_size, setValidationSetSize] = React.useState("");
    const [project_id, setProjectId] = React.useState("");  // [TODO] get project id from props
    const [annotations, setAnnotations] = React.useState(null);
 

    const handleClickOpen = () => {
        setOpen(true);
    }

    const handleClose = () => {
        setOpen(false);
    }

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setAnnotations(file);
    };


    const handleSave = async (event) => {
        event.preventDefault();
        const formData = new FormData();

        const dataJson = {
            name,
            architecture,
            learning_rate,
            weight_decay,
            epochs,
            validation_set_size,
          };
        

        formData.append('file', annotations);
        formData.append('data', JSON.stringify(dataJson));
        

        // try {
        //     const response = await fetch('/api/create_model', {
        //       method: 'POST',
        //       headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
        //       },
        //       body: JSON.stringify({
        //         name,
        //         architecture,
        //         learning_rate,
        //         weight_decay,
        //         epochs,
        //         validation_set_size,
        //       }),
        //     });
      
        //     if (!response.ok) {
        //       const error = await response.json();
        //       setError(error.detail);
        //       return;
        //     }
        //     setOpen(false);
        //     props.onClose(true);
        //   } catch (error) {
        //     console.error('Error', error);
        //   }

        try {
            const response = await fetch('/api/upload_annotation', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
                    // 'Content-Type': 'multipart/form-data',
                },
                body: formData,
            });

            if (!response.ok) {
                // Check if the response is JSON
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const error = await response.json();
                    setError(error.detail);
                    console.log("json-error", error.detail)
                } else {
                    // If not JSON, handle the error as plain text
                    const errorText = await response.text();
                    setError(errorText);
                    console.log("text-error", errorText)
                }
            }
            console.log("success?", response.status)
            setOpen(false);
            props.onClose(true);
        } catch (error) {
            console.error('Error', error);
        }
    };

    return (
        <React.Fragment>
            <Button variant="outlined" onClick={handleClickOpen}>
                Create Model
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
                            Create Model
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
                            label="name"
                            id="fullWidth"
                            onChange={(event) => setName(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <Select
                            required
                            fullWidth
                            id="fullWidth"
                            onChange={(event) => setArchitecture(event.target.value)}
                            value={architecture}
                            displayEmpty
                        >
                            <MenuItem value="" disabled >
                                <em>architecture</em>
                            </MenuItem>
                            <MenuItem value={10}>Faster RCNN</MenuItem>
                            {/* <MenuItem value={20}>model 2</MenuItem> */}
                            {/* <MenuItem value={30}>model 3</MenuItem> */}
                        </Select>
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="learning rate"
                            id="fullWidth"
                            onChange={(event) => setLearningRate(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="weight decay"
                            id="fullWidth"
                            onChange={(event) => setWeightDecay(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="number of epochs"
                            id="fullWidth"
                            onChange={(event) => setEpochs(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="validation set size"
                            id="fullWidth"
                            onChange={(event) => setValidationSetSize(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <input
                            required
                            type="file"
                            accept=".json"
                            onChange={handleFileChange}
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
