import * as React from 'react';
import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import Tooltip from '@mui/material/Tooltip';

const HelpIconWithTooltip = ({ title }) => {
  return (
    <Tooltip 
      title={title}
      placement="top"
      arrow
      sx={{
        fontSize: '1.2rem', // adjust icon size
      }}
    >
      <HelpRoundedIcon />
    </Tooltip>
  );
};

export default HelpIconWithTooltip;