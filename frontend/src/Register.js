import React, { useState } from "react";
import "./Register.css";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fullname: fullName,
        email: email,
        password: password
      })
    });

    const data = await response.json();
    setMessage(data.message);

    if (response.ok) {
      setFullName("");
      setEmail("");
      setPassword("");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1500);
    }
  };

  return (
   


    <div className="register-container">
      <h2>Register</h2>
      <p className="register-intro">
  Welcome to <strong>MediGuard</strong> 
</p>

      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      <p className="register-footer">
  © 2025 MediGuard. Empowering Elderly Care with Technology.
</p>

      <p>{message}</p>
    </div>
  );
}

export default Register;
