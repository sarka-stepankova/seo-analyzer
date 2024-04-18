import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const MetaDescriptionAnalysis = ({ report }) => {
  let mainSentence;
  if (report.meta_description_length === 0) {
    mainSentence = "Meta description was NOT found.";
  } else {
    mainSentence = `Meta description was found and it is ${report.meta_description_length} characters long.`;
  }

  const additionalSentence = report.meta_description_length_test === 'passed'
    ? 'Which is good.'
    : 'Meta description should be between 50 and 160 characters long. Like title tags, meta descriptions should accurately reflect the content of the page and include relevant keywords. This helps users understand what the page is about and can improve click-through rates (CTR) from search results.';

  return (
    <div style={{ paddingTop: '20px' }}>
      <Typography>
        <span style={{ fontWeight: 'bold' }}>Meta description <HelpIconWithTooltip title="Analysis of your page's meta description" />:</span>
        <br />
        {report.meta_description_length !== 0 && (
          <>
            <span style={{ fontWeight: 'bold', fontFamily: 'monospace' }}>{report.meta_description}</span>
            <br />
          </>
        )}
        <IconBasedOnReport report_test={report.meta_description_length_test}/> {mainSentence} {additionalSentence}
      </Typography>
    </div>
  );
};

export default MetaDescriptionAnalysis;

