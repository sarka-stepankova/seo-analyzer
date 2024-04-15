import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    passed: {
      main: '#4caf50',
    },
    warning: {
      main: '#ff9800',
    },
    failed: {
      main: '#f44336',
    },
    typography: {
      allVariants: {
        color: "#243B53"
      },
    },
  },
});

export default theme;
