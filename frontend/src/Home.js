import React from 'react';
import './Home.css';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to MediGuard</h1>
      <p>Your health assistant for daily medication tracking</p>
      <div className="button-group">
        <Link to="/add-patient" className="home-button">➕ Add Patient</Link>
        <Link to="/add-medication" className="home-button">💊 Add Medication</Link>
        <Link to="/view-medications" className="home-button">📋 View Schedule</Link>
        <Link to="/view-patients" className="home-button">👤 View Patients</Link>
        <footer className="footer">
  © 2025 MediGuard. Empowering Elderly Care with Technology.
</footer>

      </div>
    </div>
  );
}

export default Home;
