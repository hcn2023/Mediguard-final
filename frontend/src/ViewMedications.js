import React, { useEffect, useState } from "react";
import "./ViewMedications.css";

function ViewMedications() {
  const [medications, setMedications] = useState([]);
  const [error, setError] = useState(false);

  const fetchMedications = () => {
    fetch("http://127.0.0.1:5000/api/view_medications")
      .then((response) => {
        if (!response.ok) throw new Error("Failed");
        return response.json();
      })
      .then((data) => {
        setMedications(data);
        setError(false);
      })
      .catch(() => {
        setError(true);
      });
  };

  useEffect(() => {
    fetchMedications();
  }, []);

  const toggleTaken = async (medId, currentStatus) => {
    const newStatus = currentStatus === "Yes" ? "No" : "Yes";

    const response = await fetch(`http://127.0.0.1:5000/api/update_medication/${medId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ taken: newStatus })
    });

    const data = await response.json();
    alert(data.message);
    fetchMedications();
  };

  // ✅ Check if any medication has not been taken
  const hasPendingMeds = medications.some((m) => m.taken === "No");

  return (
    <div className="view-container">
      <h2>Medication List</h2>

      {hasPendingMeds && (
        <div className="reminder-box">
          🔔 Reminder: Some medications have not been taken. Please follow up!
        </div>
      )}

      {error ? (
        <p style={{ color: "red" }}>Error loading data.</p>
      ) : medications.length === 0 ? (
        <p>No medications found.</p>
      ) : (
        <ul>
          {medications.map((m) => (
            <li key={m.id}>
              Patient ID: {m.patient_id} | {m.medication} – Dosage: {m.dosage} – Taken: {m.taken}{" "}
              <button onClick={() => toggleTaken(m.id, m.taken)}>
                {m.taken === "Yes" ? "Mark as Not Taken" : "Mark as Taken"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ViewMedications;
