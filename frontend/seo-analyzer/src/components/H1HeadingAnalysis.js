import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const H1HeadingAnalysis = ({ report }) => {
  const additionalSentence = report.h1_number_test === 'passed'
    ? 'You have one H1 tag, that is perfect. Ensure your most important keywords appear in the H1 tag - don\'t force it.'
    : 'Bad number of H1 tags found on your homepage (' + report.h1_number + '). For the best SEO results there should be exactly one H1 tag on each page.';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>H1 Heading</span> <HelpIconWithTooltip title="Analysis of the number of your H1 tags on page." />:
      <br />
      <IconBasedOnReport report_test={report.h1_number_test}/> {additionalSentence}
    </Typography>
    </div>
  );
};

export default H1HeadingAnalysis;
