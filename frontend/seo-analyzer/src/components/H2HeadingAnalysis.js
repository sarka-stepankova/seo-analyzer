import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const H1HeadingAnalysis = ({ report }) => {
  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>H2 Heading <HelpIconWithTooltip title="Informative Analysis of the number of your H2 tags on page." />:</span>
      <br />
      <IconBasedOnReport report_test={report.h2_number_test}/> You have {report.h2_number} H2 tags on your page. The number of H2 tags does not matter that much. Use them to structure your page so it flows better.
    </Typography>
    </div>
  );
};

export default H1HeadingAnalysis;
