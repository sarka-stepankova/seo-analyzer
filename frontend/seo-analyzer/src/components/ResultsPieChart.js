import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

const ResultsPie = ({ report }) => {
  // Extracting data from the report object
  const { passed, warning, failed } = report;

  return (
    <PieChart
      colors={['#58BB58', '#F7CA63', '#ED6A5E']}
      series={[
        {
          data: [
            { id: 0, value: passed, label: 'Passed (' + passed + ')' },
            { id: 1, value: warning, label: 'Warning (' + warning + ')' },
            { id: 2, value: failed, label: 'Failed (' + failed + ')' },
          ],
        },
      ]}
      width={400}
      height={200}
    />
  );
};

export default ResultsPie;
