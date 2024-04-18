import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const ResponseTimeAnalysis = ({ report }) => {
  const additionalSentence = report.response_time_test === 'passed'
    ? 'It is under 0.2 seconds which is great.'
    : 'Ideally, keep the response time under 0.2 seconds.';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Response Time <HelpIconWithTooltip title="How fast does your server respond to requests?" />:</span>
      <br />
      <IconBasedOnReport report_test={report.response_time_test}/> Your response time is {report.response_time.toFixed(2)} seconds. {additionalSentence}
    </Typography>
    </div>
  );
};

export default ResponseTimeAnalysis;
