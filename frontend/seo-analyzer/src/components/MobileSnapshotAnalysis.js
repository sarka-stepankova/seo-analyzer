import * as React from 'react';
import Typography from '@mui/material/Typography';
import IconBasedOnReport from './IconBasedOnReport';

const MobileSnapshotAnalysis = ({ report }) => {
  // using timestamp for image displaying
  // otherwise the old image is cached in browser and displayed
  const timestamp = new Date().getTime();

  return (
    <div>
      <Typography>
        <span style={{ fontWeight: 'bold' }}>Mobile Snapshot:</span> 
        <br />
        <IconBasedOnReport report_test={report.mobile_snapshot_path_test}/> Here is how your site may appear on a mobile device.
        <br />
        {/* Construct the URL to the image served from the backend */}
        {report.mobile_snapshot_path && (
          <div style={{ position: 'relative', width: '50%', margin: '20px auto', borderRadius: '20px', border: '2px solid #ccc', boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.1)', padding: '3px' }}>
            {/* Mobile phone frame */}
            <div style={{ position: 'absolute', top: '5px', left: '5px', right: '5px', bottom: '5px', border: '2px solid #aaa', borderRadius: '15px' }}></div>
            {/* Image */}
            <img src={`http://localhost:5000/images/mobile-snapshot.png?timestamp=${timestamp}`} alt="Mobile Snapshot" style={{ width: '100%', height: 'auto', borderRadius: '15px' }} />
          </div>
        )}
        {/* Show a placeholder or message if mobile_snapshot_path is not available */}
        {!report.mobile_snapshot_path && (
          <span>No mobile snapshot available</span>
        )}
      </Typography>
    </div>
  );
};
  
export default MobileSnapshotAnalysis;
