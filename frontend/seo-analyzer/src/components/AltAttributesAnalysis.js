// import * as React from 'react';
// import Typography from '@mui/material/Typography';
// import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
// import IconBasedOnReport from './IconBasedOnReport';

// const AltAttributesAnalysis = ({ report }) => {
//   const additionalSentence = report.images_without_alt_number_test === 'passed'
//     ? 'All images have alt attribute, nice! You can check the usefulness of your alt description.'
//     : 'Some images on your homepage have no alt attribute. (' + report.images_without_alt_number + '). Check your images for missing alt tags, and add useful descriptions to each image.';

//   const image_names = report.images_without_alt.slice(0, 5); // Take the first 3 images

//   return (
//     <div style={{ paddingTop: '20px' }}>
//     <Typography>
//       <span style={{ fontWeight: 'bold' }}>Image ALT Attributes</span> <HelpIconWithTooltip title="Analysis of the number of missing image alt attributes." />:
//       <br /> 
//       <IconBasedOnReport report_test={report.images_without_alt_number_test}/> {additionalSentence}
//       <br /> 
//       Some of them:
//     </Typography>
//     <div style={{ 
//         marginTop: '10px', 
//         fontFamily: 'monospace', 
//         border: '1px solid #ccc', 
//         padding: '10px', 
//         borderRadius: '4px', 
//         whiteSpace: 'nowrap', // Prevent wrapping
//         overflowX: 'auto' // Make the container scrollable horizontally
//       }}>
//         {image_names.map((image, index) => (
//           <div key={index} style={{ marginBottom: '10px' }}>
//             <code>{`<img class="d-block atm-picture__img atm-picture__img--loaded" src="${image}" alt="">`}</code>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default AltAttributesAnalysis;


import * as React from 'react';
import Typography from '@mui/material/Typography';
import HelpIconWithTooltip from './HelpIconRoundWithTooltip';
import IconBasedOnReport from './IconBasedOnReport';

const AltAttributesAnalysis = ({ report }) => {
  if (report.images_without_alt_number_test === 'passed') {
    const additionalSentence = 'All images have alt attribute, nice! You can check the usefulness of your alt descriptions.';

    return (
      <div style={{ paddingTop: '20px' }}>
        <Typography>
          <span style={{ fontWeight: 'bold' }}>Image ALT Attributes</span> <HelpIconWithTooltip title="Analysis of the number of missing image alt attributes." />:
          <br /> 
          <IconBasedOnReport report_test={report.images_without_alt_number_test}/> {additionalSentence}
        </Typography>
      </div>
    );
  }

  const additionalSentence = `Some images on your homepage have no alt attribute. (${report.images_without_alt_number}). Check your images for missing alt tags, and add useful descriptions to each image.`;
  const imageNames = report.images_without_alt.slice(0, 5); // Take the first 5 images

  return (
    <div style={{ paddingTop: '20px' }}>
      <Typography>
        <span style={{ fontWeight: 'bold' }}>Image ALT Attributes</span> <HelpIconWithTooltip title="Analysis of the number of missing image alt attributes." />:
        <br /> 
        <IconBasedOnReport report_test={report.images_without_alt_number_test}/> {additionalSentence}
        <br /> 
        Some of them:
      </Typography>
      <div style={{ 
        marginTop: '10px', 
        fontFamily: 'monospace', 
        border: '1px solid #ccc', 
        padding: '10px', 
        borderRadius: '4px', 
        whiteSpace: 'nowrap', // Prevent wrapping
        overflowX: 'auto' // Make the container scrollable horizontally
      }}>
        {imageNames.map((image, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <code>{`<img src="${image}" alt="">`}</code>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AltAttributesAnalysis;
