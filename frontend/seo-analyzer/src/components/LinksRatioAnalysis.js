import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const LinksRatioAnalysis = ({ report }) => {
  return (
    <div style={{ paddingTop: '20px' }}>
    <Typography>
      <span style={{ fontWeight: 'bold' }}>Links Ratio <HelpIconWithTooltip title="Analysis of the ratio of internal links to external links." />:</span>
      <br />
      <span style={{ fontWeight: 'bold', fontFamily: 'monospace' }}>
        internal: {report.internal_links_number}<br />
        external: {report.external_links_number}<br />
      </span>
      <IconBasedOnReport report_test={report.links_number_ratio_test}/>
      Your homepage has {report.internal_links_number} internal and {report.external_links_number} external links. As for the ratio, there isn't a strict rule, but a common recommendation is to have more internal links than external links. A rough guideline could be to aim for a ratio of around 2:1 or 3:1 of internal links to external links. However, the most important factor is the relevance and context of the links rather than the specific ratio.
    </Typography>
    </div>
  );
};

export default LinksRatioAnalysis;
