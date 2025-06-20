import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AddPatient from './AddPatient';
import Register from './Register';
import Login from './login';
import Home from './Home';
import AddMedication from './AddMedication';
import ViewMedications from './ViewMedications';
import ViewPatients from './ViewPatients';


function App() {
  return (
    <Router>
      <Routes>
        
        <Route path="/add-patient" element={<AddPatient />} />
        <Route path="/" element={<Navigate to="/register" />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/add-medication" element={<AddMedication />} />
        <Route path="/view-medications" element={<ViewMedications />} />
        <Route path="/view-schedule" element={<ViewMedications />} />
        <Route path="/view-patients" element={<ViewPatients />} />
        

      </Routes>
    </Router>
  );
}

export default App;
