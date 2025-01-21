import reportWebVitals from './reportWebVitals';
import React from 'react';
import ReactDOM from 'react-dom/client';  // Use this import for React 18 and later
import App from './App';
import { UserProvider } from './UserContext'; // Import UserProvider

// Create a root for rendering the app
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App wrapped with the UserProvider
root.render(
  <UserProvider>
    <App />
  </UserProvider>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
