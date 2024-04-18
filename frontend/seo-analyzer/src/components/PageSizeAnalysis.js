import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const PageSizeAnalysis = ({ report }) => {
  const additionalSentence = report.page_size_test === 'passed'
    ? 'This is good, because it is recommended to keep the size of the HTML page to 100 kB or less.'
    : 'Ideally, keep the HTML page size around 100 kB or less. In some cases (like ecommerce) it\'s ok to have pages around 150 kB - 200 kB.';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Page Size <HelpIconWithTooltip title="Analysis of the size of your HTML file." />:</span>
      <br />
      <IconBasedOnReport report_test={report.page_size_test}/> The size of the HTML document is {Math.floor(report.page_size)} kB. {additionalSentence}
    </Typography>
    </div>
  );
};

export default PageSizeAnalysis;
