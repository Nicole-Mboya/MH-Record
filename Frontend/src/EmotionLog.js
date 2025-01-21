// EmotionLogs.js
import React, { useState, useEffect } from 'react';

function EmotionLogs() {
  const [emotionLogs, setEmotionLogs] = useState([]);

  useEffect(() => {
    const fetchEmotionLogs = async () => {
      const response = await fetch('/api/emotion-logs/', {
        method: 'GET',
        credentials: 'include',  // Ensures the session cookie is sent
      });

      if (response.ok) {
        const data = await response.json();
        setEmotionLogs(data);
      }
    };

    fetchEmotionLogs();
  }, []);

  return (
    <div>
      <h2>Emotion Logs</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Emotion</th>
          </tr>
        </thead>
        <tbody>
          {emotionLogs.map((log, index) => (
            <tr key={index}>
              <td>{new Date(log.created_at).toLocaleString()}</td>
              <td>{log.emotion}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EmotionLogs;
