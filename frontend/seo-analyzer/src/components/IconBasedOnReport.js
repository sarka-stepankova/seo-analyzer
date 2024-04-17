import * as React from 'react';
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded';
import ErrorRoundedIcon from '@mui/icons-material/ErrorRounded';
import CancelRoundedIcon from '@mui/icons-material/CancelRounded';
import InfoIcon from '@mui/icons-material/Info';

const IconBasedOnReport = ({ report_test }) => {
  let iconComponent;

  if (report_test === 'passed') {
    iconComponent = <CheckCircleRoundedIcon sx={{ fontSize: '1.4rem', color: '#4CAF50' }} />;
  } else if (report_test === 'warning') {
    iconComponent = <ErrorRoundedIcon sx={{ fontSize: '1.4rem', color: '#E3A127' }} />;
  } else if (report_test === 'failed') {
    iconComponent = <CancelRoundedIcon sx={{ fontSize: '1.4rem', color: '#F44336' }} />;
  } else { // informative
    iconComponent = <InfoIcon sx={{ fontSize: '1.4rem', color: '#069DE3' }} />;
  }

  return iconComponent;
};

export default IconBasedOnReport;
