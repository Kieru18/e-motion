import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Box, Button, Container, Grid, Paper, Select, MenuItem, Typography, FormHelperText, InputLabel, FormControl } from "@mui/material";
import Stack from '@mui/material/Stack';


const ModelSelect = (props) => {
  const [models, setModels] = useState(props.models);
  const [selected, setSelected] = useState("");

  const handleSelect = (event) => {
    setSelected(event.target.value);
    props.sendSelectedId(event.target.value.id);
  };

  return (
    <Grid item xs={4}>
      <FormControl required>
        <InputLabel id="select-model-helper-label">Model</InputLabel>
        <Select
          required
          displayEmpty
          labelId="select-model-helper-label"
          value={selected}
          label="Model"
          style={{ width: 200 }}
          onChange={handleSelect}
        >
          {models.map((model) => (
            <MenuItem key={model.id} value={model}>
              {model.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormHelperText>Select model</FormHelperText>
    </Grid>
  );
};

export default function MakePredictionsPage(props) {
  const navigate = useNavigate();
  const location = useLocation();
  const [canDownload, setCanDownload] = useState(false);
  const [models, setModels] = useState([{"id": 0, "name": "M1"}]);
  const [project_id, setProject_id] = useState(location.state.project_id);
  const [selected_id, setSelectedId] = useState(null);

  const fetchModels = () => {
    fetch(`/api/list_models/${project_id}/`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch models");
      }
      return response.json();
    })
    .then((data) => {
      if (data.length === 0) {
        console.log("No models found", data.length);
        navigate('/dashboard'); // Redirect to '/dashboard' if models array is empty
      } else {
        console.log("Models found", data.length);
        setModels(data);
      }
    })
    .catch((error) => console.log(error));
  };

  // fetch models when component is mounted
  // React.useEffect(() => {
  //   fetchModels();
  // }, []);

  const handleMakePrecition = () => {
    fetch(`/api/make_predictions/${project_id}/${selected_id}/`, {
      method: "GET",
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
      // body: JSON.stringify({
      //   project_id,
      //   selected_id,
      // }),
    })
    .then(response => {
      if (response.ok) {
          return response.blob();
      } else {
          console.error('File download failed.');
      }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `annotations.json`;
        document.body.appendChild(link);
        link.click();
        // Cleanup
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
    });
  };

  const handleFileDownload = () => {
    const requestOptions = {
      method: "GET",
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    };
    fetch('/api/make_predictions', requestOptions)
      .then(response => {
          if (response.ok) {
              return response.blob();
          } else {
              console.error('File download failed.');
          }
      })
      .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `annotations.json`;
          document.body.appendChild(link);
          link.click();
          // Cleanup
          window.URL.revokeObjectURL(url);
      })
      .catch(error => {
          console.error('Error:', error);
      });
  };

  const getSelectedId = (value) => {
    setSelectedId(value);
  };

  return (
    <Container>
      <Stack spacing={3}>
        <Box padding={3} textAlign="center">
          <Typography variant="h1" >
            Choose your ML model
          </Typography>
        </Box>
        <Box padding={15}>
          <Grid container spacing={5} justifyContent="center" alignItems="center">
            <ModelSelect models={models} sendSelectedId={getSelectedId}></ModelSelect>
            {/* Make predictions button */}
            <Grid item xs={4}>
              <Button
                variant="contained"
                onClick={handleMakePrecition}
              >
                Make predictions!
              </Button>
            </Grid>
            {/* BUTTON NIEPOTRZEBNY PO MAKEPREDICTIONS MOZE OD RAZU BYC POBIERANY JSON */}
            {/* Download Annotations button */}
            {/* <Grid item xs={4} md={4} lg={3}>
              <Button
                variant="contained"
                component="label"
                disabled={!canDownload}
                startIcon={<DownloadIcon />}
                onClick={handleFileDownload}
              >
                Download Annotations
              </Button>
            </Grid> */}
          </Grid>
        </Box>
      </Stack>
    </Container>
  );
}