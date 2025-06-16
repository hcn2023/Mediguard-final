import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/ping')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => {
        setMessage('Error connecting to backend');
        console.error('Error:', error);
      });
  }, []);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: 'linear-gradient(to right, #a8edea, #fed6e3)',
      fontFamily: 'Arial'
    }}>
      <h1 style={{ color: '#222' }}>MediGuard Frontend</h1>
      <p style={{ fontSize: '20px', color: '#555' }}>{message}</p>
    </div>
  );
}

export default App;
