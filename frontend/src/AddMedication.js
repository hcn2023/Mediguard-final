import React, { useState, useEffect } from "react";
import "./AddMedication.css";

function AddMedication() {
  const [patientId, setPatientId] = useState("");
  const [medication, setMedication] = useState("");
  const [dosage, setDosage] = useState("");
  const [patients, setPatients] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/view_patients")
      .then((res) => res.json())
      .then((data) => setPatients(data));
  }, []);

  const handleAddMedication = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/api/add_medication", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_id: patientId, medication, dosage, taken: "No" })
    });

    const data = await response.json();
    setMessage(data.message);

    if (response.ok) {
      setPatientId("");
      setMedication("");
      setDosage("");
    }
  };

  return (
    <div className="add-medication-container">
      <h2>Add Medication</h2>
      <form onSubmit={handleAddMedication}>
        <select value={patientId} onChange={(e) => setPatientId(e.target.value)} required>
          <option value="">Select Patient</option>
          {patients.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
        <input type="text" placeholder="Medication Name" value={medication} onChange={(e) => setMedication(e.target.value)} required />
        <input type="text" placeholder="Dosage" value={dosage} onChange={(e) => setDosage(e.target.value)} required />
        <button type="submit">Add Medication</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default AddMedication;
