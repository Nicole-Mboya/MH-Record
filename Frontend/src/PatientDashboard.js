// PatientDashboard.js
import React, { useState } from 'react';
import EmotionLogs from './EmotionLogs';
import JournalEntries from './JournalEntries';
import EmotionChart from './EmotionChart';

function PatientDashboard() {
  const [activeTab, setActiveTab] = useState('emotion-logs');

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="dashboard">
      <div className="tabs">
        <button onClick={() => handleTabChange('emotion-logs')}>Emotion Logs</button>
        <button onClick={() => handleTabChange('journaling')}>Journaling</button>
        <button onClick={() => handleTabChange('emotion-chart')}>Emotions Over Time</button>
      </div>

      {activeTab === 'emotion-logs' && <EmotionLogs />}
      {activeTab === 'journaling' && <JournalEntries />}
      {activeTab === 'emotion-chart' && <EmotionChart />}
    </div>
  );
}

export default PatientDashboard;
