import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const SecureConnAnalysis = ({ report }) => {
  const additionalSentence = report.https_enabled_test === 'passed'
    ? 'Your site is using a secure transfer protocol (https).'
    : 'Your site is NOT using a secure transfer protocol (https).';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Secure Connection <HelpIconWithTooltip title="Is your content served over a secure connection?" />:</span>
      <br />
      <IconBasedOnReport report_test={report.https_enabled_test}/> {additionalSentence}
    </Typography>
    </div>
  );
};

export default SecureConnAnalysis;
