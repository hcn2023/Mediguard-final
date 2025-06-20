import React, { useEffect, useState } from "react";
import "./ViewPatients.css";

function ViewPatients() {
  const [patients, setPatients] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/view_patients")
      .then((response) => {
        if (!response.ok) throw new Error("Failed");
        return response.json();
      })
      .then((data) => {
        setPatients(data);
        setError(false);
      })
      .catch(() => {
        setError(true);
      });
  }, []);

  return (
    <div className="view-container">
      <h2>Patient List</h2>
      {error ? (
        <p style={{ color: "red" }}>Error loading patients.</p>
      ) : patients.length === 0 ? (
        <p>No patients found.</p>
      ) : (
        <ul>
          {patients.map((p) => (
            <li key={p.id}>
              <strong>{p.name}</strong> (Age: {p.age}) – {p.condition}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ViewPatients;
