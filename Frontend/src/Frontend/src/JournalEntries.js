// JournalEntries.js
import React, { useState, useEffect } from 'react';

function JournalEntries() {
  const [entries, setEntries] = useState([]);
  const [textContent, setTextContent] = useState('');
  const [image, setImage] = useState(null);

  useEffect(() => {
    const fetchEntries = async () => {
      const response = await fetch('/api/journal-entries/', {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setEntries(data);
      }
    };
    fetchEntries();
  }, []);

  const handleAddJournalEntry = async () => {
    if (!textContent) return;

    const formData = new FormData();
    formData.append('text_content', textContent);
    if (image) formData.append('image', image);

    const response = await fetch('/api/journal-entries/', {
      method: 'POST',
      body: formData,
      credentials: 'include',
    });

    if (response.ok) {
      setEntries([{ text_content: textContent, image }, ...entries]);
      setTextContent('');
      setImage(null);
    }
  };

  return (
    <div>
      <h1>Journaling</h1>
      <textarea
        value={textContent}
        onChange={(e) => setTextContent(e.target.value)}
        placeholder="Write your journal entry..."
      />
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <button onClick={handleAddJournalEntry}>Add Journal Entry</button>

      <div>
        {entries.map((entry, index) => (
          <div key={index}>
            <p>{entry.text_content}</p>
            {entry.image && <img src={entry.image} alt="Journal Image" />}
          </div>
        ))}
      </div>
    </div>
  );
}

export default JournalEntries;
