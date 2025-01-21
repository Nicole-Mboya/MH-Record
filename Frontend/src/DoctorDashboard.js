import React, { useState, useEffect } from 'react';

function DoctorDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [newAppointment, setNewAppointment] = useState({ patient_id: '', date: '', notes: '' });
  const [appointmentNotes, setAppointmentNotes] = useState('');
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    // Fetch appointments for the logged-in doctor
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    setIsFetching(true);
    const response = await fetch('/api/appointments/', {
      method: 'GET',
      credentials: 'include', // Include session cookies with request
    });

    if (response.ok) {
      const data = await response.json();
      setAppointments(data);
    } else {
      console.log('Error fetching appointments');
    }
    setIsFetching(false);
  };

  const addAppointment = async () => {
    const response = await fetch('/api/appointments/add_appointment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newAppointment),
      credentials: 'include', // Include session cookies with request
    });

    if (response.ok) {
      fetchAppointments();
    } else {
      console.log('Error adding appointment');
    }
  };

  const cancelAppointment = async (id) => {
    const response = await fetch(`/api/appointments/${id}/cancel_appointment/`, {
      method: 'POST',
      credentials: 'include', // Include session cookies with request
    });

    if (response.ok) {
      fetchAppointments();
    } else {
      console.log('Error canceling appointment');
    }
  };

  const addAppointmentNote = async (appointmentId) => {
    const response = await fetch(`/api/appointment-notes/${appointmentId}/add_note/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ note: appointmentNotes }),
      credentials: 'include', // Include session cookies with request
    });

    if (response.ok) {
      fetchAppointments();
    } else {
      console.log('Error adding appointment note');
    }
  };

  return (
    <div>
      <h1>Doctor's Dashboard</h1>
      <div>
        <h2>Appointments</h2>
        {isFetching ? (
          <p>Loading appointments...</p>
        ) : (
          appointments.map((appointment) => (
            <div key={appointment.id}>
              <h3>Appointment with {appointment.patient.user.username} on {appointment.date}</h3>
              <button onClick={() => cancelAppointment(appointment.id)}>Cancel Appointment</button>
              <div>
                <textarea
                  value={appointmentNotes}
                  onChange={(e) => setAppointmentNotes(e.target.value)}
                  placeholder="Add notes..."
                />
                <button onClick={() => addAppointmentNote(appointment.id)}>Add Note</button>
              </div>
            </div>
          ))
        )}
      </div>

      <div>
        <h2>Add New Appointment</h2>
        <input
          type="text"
          placeholder="Patient ID"
          value={newAppointment.patient_id}
          onChange={(e) => setNewAppointment({ ...newAppointment, patient_id: e.target.value })}
        />
        <input
          type="datetime-local"
          value={newAppointment.date}
          onChange={(e) => setNewAppointment({ ...newAppointment, date: e.target.value })}
        />
        <textarea
          value={newAppointment.notes}
          onChange={(e) => setNewAppointment({ ...newAppointment, notes: e.target.value })}
          placeholder="Notes"
        />
        <button onClick={addAppointment}>Add Appointment</button>
      </div>
    </div>
  );
}

export default DoctorDashboard;
