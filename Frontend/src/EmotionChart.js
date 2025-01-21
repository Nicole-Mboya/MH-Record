// EmotionChart.js
import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

function EmotionChart() {
  const [chartData, setChartData] = useState(null);
  const [days, setDays] = useState(7); // Default to 7 days

  useEffect(() => {
    const fetchEmotionData = async () => {
      const response = await fetch(`/api/emotion-log-chart/${days}/`, {
        method: 'GET',
        credentials: 'include',  // Ensures the session cookie is sent
      });

      if (response.ok) {
        const data = await response.json();
        setChartData(data);
      }
    };

    fetchEmotionData();
  }, [days]);

  const handleDaysChange = (event) => {
    setDays(event.target.value);
  };

  if (!chartData) {
    return <p>Loading chart...</p>;
  }

  return (
    <div>
      <h1>Emotions Over Time</h1>
      <select onChange={handleDaysChange} value={days}>
        <option value={7}>Last 7 Days</option>
        <option value={30}>Last 30 Days</option>
      </select>
      
      <Bar
        data={chartData}
        options={{
          responsive: true,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Date',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Number of Entries',
              },
              beginAtZero: true,
            },
          },
        }}
      />
    </div>
  );
}

export default EmotionChart;
