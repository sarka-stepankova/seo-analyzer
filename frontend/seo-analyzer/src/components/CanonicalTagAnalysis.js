import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const CanonicalTagAnalysis = ({ report }) => {

  const additionalSentence = report.meta_description_length_test === 'passed'
    ? `You page is using the canonical link tag (${report.canonical_url}).`
    : 'Your page is NOT using the canonical link tag. It\'s recommended to have one.';

  return (
    <div style={{ paddingTop: '20px' }}>
      <Typography>
        <span style={{ fontWeight: 'bold' }}>Meta description <HelpIconWithTooltip title="Does your page have canocial url?" />:</span>
        <br />
        <IconBasedOnReport report_test={report.canonical_url_test}/> {additionalSentence}
      </Typography>
    </div>
  );
};

export default CanonicalTagAnalysis;

