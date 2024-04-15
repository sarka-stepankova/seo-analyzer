import React from 'react';
import AnalysisForm from './components/AnalysisForm';
import { ThemeProvider } from '@mui/material/styles';
import theme from './themes/customTheme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <AnalysisForm />
      </div>
    </ThemeProvider>
  );
}

export default App;
