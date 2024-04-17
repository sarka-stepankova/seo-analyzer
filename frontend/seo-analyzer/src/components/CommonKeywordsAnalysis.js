import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const CommonKeywordsAnalysis = ({ report }) => {
  const keywordFrequency = report.keyword_frequency;

  if (!keywordFrequency || keywordFrequency.length === 0) {
    return null; // If there are no keywords, don't render anything
  }

  return (
    <div style={{ paddingTop: '20px' }}>
      <Typography>
        <span style={{ fontWeight: 'bold' }}>Common Keywords</span> <HelpIconWithTooltip title="A list of 10 keywords that appear frequently in the text of your content." />:
        <br />
      </Typography>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {keywordFrequency.map((keyword, index) => (
          <div key={index} style={{ margin: '5px', padding: '5px', background: '#f0f0f0', borderRadius: '4px' }}>
            <span style={{ fontSize: '16px' }}>
              {keyword[0]}
            </span>
          </div>
        ))}
      </div>
      <Typography>
      <IconBasedOnReport report_test={report.most_common_keywords_test}/> These are the 10 most common keywords found on the page.
      </Typography>
    </div>
  );
};

export default CommonKeywordsAnalysis;
