import React, { useState, useEffect } from 'react';

function PatientRecords() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPatientRecords = async () => {
      const response = await fetch('/api/patient-records/', {
        method: 'GET',
        credentials: 'include', // Ensure session cookies are sent
      });
      if (response.ok) {
        const data = await response.json();
        setPatients(data);
      } else {
        console.error('Failed to fetch patient records');
      }
      setLoading(false);
    };
    fetchPatientRecords();
  }, []);

  return (
    <div>
      <h1>Patient Records</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Upcoming Appointments</th>
              <th>Patient Notes</th>
              <th>Mental Health History</th>
            </tr>
          </thead>
          <tbody>
            {patients.map(patient => (
              <tr key={patient.patient_id}>
                <td>{patient.patient_name}</td>
                <td>{patient.age}</td>
                <td>{patient.gender}</td>
                <td>
                  {patient.appointments.map((appointment, index) => (
                    <div key={index}>
                      {appointment.date} - {appointment.is_cancelled ? 'Cancelled' : 'Scheduled'}
                    </div>
                  ))}
                </td>
                <td>
                  {patient.notes.map((note, index) => (
                    <div key={index}>{note.note}</div>
                  ))}
                </td>
                <td>
                  {patient.mental_health_history.map((history, index) => (
                    <div key={index}>
                      {history.date_recorded}: {history.mental_health_status}
                    </div>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PatientRecords;
