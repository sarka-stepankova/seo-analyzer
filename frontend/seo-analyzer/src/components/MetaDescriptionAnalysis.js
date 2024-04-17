import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const MetaDescriptionAnalysis = ({ report }) => {
  const additionalSentence = report.meta_description_length_test === 'passed'
    ? 'Which is good.'
    : 'Meta description should be between 50 and 160 characters long.';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Meta description</span> <HelpIconWithTooltip title="Analysis of your page's meta description" />: 
      <br />
      <span style={{ fontWeight: 'bold', fontFamily: 'monospace' }}>{report.meta_description}</span>
      <br /> 
      <IconBasedOnReport report_test={report.meta_description_length_test}/> Meta description was found and it is {report.meta_description_length} characters long. {additionalSentence}
    </Typography>
    </div>
  );
};

export default MetaDescriptionAnalysis;
