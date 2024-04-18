import * as React from 'react';
import Typography from '@mui/material/Typography';

const HeadText = ({ children }) => {
  return (
    <Typography
      variant="body1"
      component="div"
      sx={{
        backgroundColor: '#243B53',
        padding: '10px',
        marginTop: '30px',
        marginBottom: '20px',
        color: '#FFFFFC'
      }}
    >
      {children}
    </Typography>
  );
};

export default HeadText;
