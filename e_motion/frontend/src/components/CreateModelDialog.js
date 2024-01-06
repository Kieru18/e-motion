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
    const [title, setTitle] = React.useState("");
    const [description, setDescription] = React.useState("");
    const [dataset_url, setUrl] = React.useState("");

    const handleClickOpen = () => {
        setOpen(true);
    }

    const handleClose = () => {
        setOpen(false);
    }

    const handleSave = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('/api/create_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
                },
                body: JSON.stringify({
                    name,
                    lr,
                    weight_decay,
                    epochs,
                    val_set_size,
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                setError(error.detail);
                return;
            }
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
                        <Select
                            required
                            fullWidth
                            id="fullWidth"
                            onChange={(event) => setTitle(event.target.value)}
                            value={title}
                            displayEmpty
                        >
                            <MenuItem value="" disabled >
                                <em>name</em>
                            </MenuItem>
                            <MenuItem value={10}>model 1</MenuItem>
                            <MenuItem value={20}>model 2</MenuItem>
                            <MenuItem value={30}>model 3</MenuItem>
                        </Select>
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="learning rate"
                            id="fullWidth"
                            onChange={(event) => setTitle(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="weight decay"
                            id="fullWidth"
                            onChange={(event) => setTitle(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="number of epochs"
                            id="fullWidth"
                            onChange={(event) => setTitle(event.target.value)}
                        />
                    </ListItem>
                    <Divider />
                    <ListItem>
                        <TextField
                            required
                            fullWidth
                            label="validation set size"
                            id="fullWidth"
                            onChange={(event) => setTitle(event.target.value)}
                        />
                    </ListItem>
                </List>
            </Dialog>
        </React.Fragment>   
    );
}
