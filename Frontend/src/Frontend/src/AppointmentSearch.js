import React, { useState } from "react";

const AppointmentSearch = ({ user }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/appointments/search/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: searchQuery, doctorId: user.id }),
      });
      const data = await response.json();
      setAppointments(data);
    } catch (err) {
      setError("Error searching appointments.");
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search by Patient ID, Name, or Date"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h3>Search Results</h3>
      <table>
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map((appointment) => (
            <tr key={appointment.id}>
              <td>{appointment.patient_name}</td>
              <td>{appointment.date}</td>
              <td>
                {/* Add action buttons here */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AppointmentSearch;
