import React, { useState } from 'react';
import { Button, TextField, Typography, Container } from '@mui/material';
import axios from 'axios';
import ResultsPie from './ResultsPieChart';
import HeadText from './HeadText';
import TitleAnalysis from './TitleAnalysis';

const AnalysisForm = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await axios.post('http://localhost:5000/analyze', { url });

      if (response.status === 200) {
        setReport(response.data);
      } else {
        setError('URL is not reachable');
      }
    } catch (error) {
      setError('Error analyzing URL');
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
      {report && (
        <div>
          <Typography variant="h6">Analysis Report:</Typography>
          <ResultsPie report={report.results} />

          <HeadText>Basic SEO</HeadText>
          <TitleAnalysis report={report} />

          <HeadText>Advanced SEO</HeadText>
        </div>
      )}
    </Container>
  );
};

export default AnalysisForm;
