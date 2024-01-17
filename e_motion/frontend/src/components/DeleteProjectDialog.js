import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import Slide from '@mui/material/Slide';
import { useSnackbar } from "notistack";
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';

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
 * DeleteProjectDialog Component
 *
 * A dialog component for confirming the deletion of a project.
 *
 * @component
 * @example
 * // Example usage:
 * <DeleteProjectDialog projectId={123} close={() => console.log('Dialog closed')} />
 *
 * @param {Object} props - The properties of the component.
 * @param {number} props.projectId - The ID of the project to be deleted.
 * @param {function} props.close - Callback function to close the parent dialog.
 * @returns {JSX.Element} Rendered DeleteProjectDialog component.
 */
export default function DeleteProjectDialog(props) {
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const { enqueueSnackbar } = useSnackbar();

    const projectId = props.projectId;
    const close = props.close; // Callback function to close EditProjectDialog

    const handleClickOpen = () => {
        setDialogOpen(true);
    };

    const handleClose = () => {
        setDialogOpen(false);
    };

    const handleDeleteProject = async () => {
        try {
            const response = await fetch('/api/delete_project', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('token')}`,  // LOCALSTORAGE
                },
                body: JSON.stringify({
                    id: projectId,
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                console.log(error.detail);
                enqueueSnackbar("Project deletion failed", { variant: "warning" });
                return;
            }
            enqueueSnackbar("Project deleted successfully", { variant: "info" });
            setDialogOpen(false);
            close();

        } catch (error) {
            console.error('Error', error);
        }

        setDialogOpen(false);
    };

    return (
        <React.Fragment>
            <Button variant="outlined" color="error" onClick={handleClickOpen}>
                Delete Project
            </Button>
            <Dialog
                open={dialogOpen}
                onClose={handleClose}
                TransitionComponent={Transition}
            >
                <DialogTitle>Confirm project deletion</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Are you sure you want to delete this project? This action is irreversible.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleDeleteProject} color="error">
                        Delete
                    </Button>
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
}
