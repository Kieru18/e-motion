import * as React from 'react';
import { useNavigate } from "react-router-dom";
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
import CircularProgress from '@mui/material/CircularProgress';

const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

export default function CreateModelDialog(props) {
    const navigate = useNavigate();
    const [open, setOpen] = React.useState(false);
    const [error, setError] = React.useState(false);
    const [name, setName] = React.useState("");
    const [architecture, setArchitecture] = React.useState("");
    const [learning_rate, setLearningRate] = React.useState("");
    const [weight_decay, setWeightDecay] = React.useState("");
    const [epochs, setEpochs] = React.useState("");
    const [validation_set_size, setValidationSetSize] = React.useState("");
    const [annotations, setAnnotations] = React.useState(null);
    const [loading, setLoading] = React.useState(false);

    const projectId = props.projectId;
    const projectTitle = props.projectTitle;

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
            miou_score: null,
            top1_score: null,
            top5_score: null,
            checkpoint: null,
            project: projectId,
        };

        formData.append('file', annotations);
        formData.append('data', JSON.stringify(dataJson));

        const learningRateFloat = parseFloat(learning_rate);
        const weightDecayFloat = parseFloat(weight_decay);
        const epochsInt = parseInt(epochs);
        const validationSetSizeFloat = parseFloat(validation_set_size);

        var modelId = null;

        try {
            const response = await fetch('/api/create_model', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
              },
              body: JSON.stringify({
                name,
                architecture,
                learning_rate: learningRateFloat,
                weight_decay: weightDecayFloat,
                epochs: epochsInt,
                validation_set_size: validationSetSizeFloat,
                project: projectId,
              }),
            });

            if (!response.ok) {
              const error = await response.json();
              setError(error.detail);
              console.log("error", error.detail)
              return;
            }
            const data = await response.json();
            modelId = data["modelId"]
          } catch (error) {
            console.error('Error', error);
          }

        try {
            const url = `/api/upload_annotation/${modelId}/`;
            const response = await fetch(url, {
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
        } catch (error) {
            console.error('Error', error);
        }

        try {
            setLoading(true);
            const trainUrl = `/api/train/${modelId}/`;
            const response = await fetch(trainUrl, {
              method: 'POST',
              headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
            },

            });
            if (!response.ok) {
              setLoading(false)
              const error = await response.json();
              setError(error.detail);
              console.log("error", error.detail)
              return;
            }
            setLoading(false);
            navigate("/results", { state: { project_id: projectId, model_id: modelId }});
            // setOpen(false);
            // props.onClose(true);
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
                            Create Model for Project {projectTitle} (id: {projectId})
                        </Typography>
                        <Button autoFocus color="inherit" onClick={handleSave}>
                            save & train
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
                            <MenuItem value={"Faster RCNN"}>Faster RCNN</MenuItem>
                            {/* <MenuItem value={20}>model 2</MenuItem> */}
                            {/* <MenuItem value={30}>model 3</MenuItem> */}
                        </Select>
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            // type="number"
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
                            // type="number"
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
                            // type="number"
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
                    {loading && (
                    <div style={{ textAlign: 'center', marginTop: 10 }}>

                        <div style={{ textAlign: 'center', marginTop: 10 }}>
                        <span style={{ marginLeft: 10, marginBottom: 20}}>Training in progress...</span>
                        </div>
                        <CircularProgress size={20} />
                    </div>
                    )}
                </List>
            </Dialog>
        </React.Fragment>
    );
}
