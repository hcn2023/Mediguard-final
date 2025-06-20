import React, { useState } from "react";
import "./AddPatient.css";

function AddPatient() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [condition, setCondition] = useState("");
  const [message, setMessage] = useState("");

  const handleAddPatient = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/api/add_patient", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, condition })
    });

    const data = await response.json();
    setMessage(data.message);

    if (response.ok) {
      setName("");
      setAge("");
      setCondition("");
    }
  };

  return (
    <div className="add-patient-container">
      <h2>Add Patient</h2>
      <form onSubmit={handleAddPatient}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="number" placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} required />
        <input type="text" placeholder="Condition" value={condition} onChange={(e) => setCondition(e.target.value)} required />
        <button type="submit">Add Patient</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default AddPatient;
