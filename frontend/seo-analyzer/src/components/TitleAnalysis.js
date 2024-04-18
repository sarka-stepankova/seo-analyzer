import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const TitleAnalysis = ({ report }) => {
  const additionalSentence = report.title_length_test === 'passed'
    ? 'Which is good. It is recommended that the title is between 30 and 60 characters long. This ensures that the entire title is visible in search engine results pages and doesn\'t get truncated. However, Google may display up to 70 characters.'
    : 'It is recommended that the title is between 30 and 60 characters long. This ensures that the entire title is visible in search engine results pages and doesn\'t get truncated. However, Google may display up to 70 characters.';

  return (
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Title <HelpIconWithTooltip title="Analysis of your site's HTML title" />:</span>
      <br />
       <span style={{ fontWeight: 'bold', fontFamily: 'monospace', backgroundColor: '#F0F4F8' }}>{report.title}</span>
      <br /> 
      <IconBasedOnReport report_test={report.title_length_test}/> Your title is {report.title_length} characters long. {additionalSentence}
    </Typography>
  );
};

export default TitleAnalysis;
