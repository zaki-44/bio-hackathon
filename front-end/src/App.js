import { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [backendData, setBackendData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from backend API
    fetch('/api/test')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setBackendData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        {loading && <p>Loading data from backend...</p>}
        {error && (
          <div>
            <p style={{ color: 'red' }}>Error connecting to backend: {error}</p>
            <p>Make sure the Flask backend is running on port 5000</p>
          </div>
        )}
        {backendData && (
          <div>
            <p style={{ color: 'green', fontWeight: 'bold' }}>
              {backendData.message}
            </p>
            <p>Status: {backendData.status}</p>
          </div>
        )}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
