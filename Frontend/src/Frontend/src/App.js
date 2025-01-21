import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Redirect } from 'react-router-dom';
import Login from './Login';
import DoctorDashboard from './DoctorDashboard';
import PatientDashboard from './PatientDashboard';
import Footer from './Footer'; 

function App() {
  const [userRole, setUserRole] = useState(null); // To store the user's role

  useEffect(() => {
    // On initial load, check if the user has a role saved in sessionStorage
    const role = sessionStorage.getItem('role');
    setUserRole(role);
  }, []);

  // PrivateRoute component checks if the user has the correct role before rendering the dashboard
  const PrivateRoute = ({ component: Component, role, ...rest }) => {
    return (
      <Route
        {...rest}
        element={userRole === role ? (
          <Component {...rest} />
        ) : (
          <Redirect to="/login" />
        )}
      />
    );
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* PrivateRoute will ensure only users with the correct role can access these pages */}
        <PrivateRoute
          path="/doctor-dashboard"
          element={<DoctorDashboard />}
          role="doctor"
        />

        <PrivateRoute
          path="/patient-dashboard"
          element={<PatientDashboard />}
          role="patient"
        />

        {/* Redirect to login if the route is unknown */}
        <Route path="/" element={<Redirect to="/login" />} />
      </Routes>
      <Footer /> {/* Footer component added at the bottom */}
    </Router>
  );
}

export default App;
