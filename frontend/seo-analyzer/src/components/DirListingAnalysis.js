import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const DirListingAnalysis = ({ report }) => {
  const additionalSentence = report.directory_listing_disabled_test === 'passed'
    ? 'Directory Listing seems to be disabled on your server.'
    : 'Directory Listing seems to be enabled on your server.';

  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Directory Listing <HelpIconWithTooltip title="Does your web server list the contents of directories?" />:</span>
      <br />
      <IconBasedOnReport report_test={report.directory_listing_disabled_test}/> {additionalSentence}
    </Typography>
    </div>
  );
};

export default DirListingAnalysis;
