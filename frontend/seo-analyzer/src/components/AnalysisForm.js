import React, { useState } from 'react';
import { Button, TextField, Typography, Container } from '@mui/material';
import axios from 'axios'; // this is used for HTTP requests

const AnalysisForm = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Send URL to Flask backend for analysis
      // const response = await axios.post('/analyze', { url });
      // console.log(response.data); // Handle analysis results

      // Send URL to Flask backend for analysis
      const response = await axios.post('http://localhost:5000/analyze', { url });

      if (response.status === 200) {
          alert(`URL name: ${response.data.title}`);
      } else {
          setError('URL is not reachable');
      }
    } catch (error) {
      setError(error.message);
    }

    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        SEO Analyzer
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Enter URL"
          fullWidth
          variant="outlined"
          value={url}
          onChange={handleInputChange}
          required
          disabled={loading}
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </Button>
      </form>
      {error && <Typography color="error">{error}</Typography>}
    </Container>
  );
};

export default AnalysisForm;
