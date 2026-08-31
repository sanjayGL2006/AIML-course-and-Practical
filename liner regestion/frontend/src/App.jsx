import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import PredictionResult from './components/PredictionResult';
import { checkHealth, predictWeight } from './services/api';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isConnected, setIsConnected] = useState(true);

  // Check Flask server health on component mount
  useEffect(() => {
    let isMounted = true;
    const verifyBackend = async () => {
      try {
        await checkHealth();
        if (isMounted) setIsConnected(true);
      } catch (err) {
        if (isMounted) setIsConnected(false);
      }
    };
    verifyBackend();
    const interval = setInterval(verifyBackend, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const handlePredict = async (height) => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await predictWeight(height);
      if (data && data.success) {
        setResult(data);
        setIsConnected(true);
      } else {
        setError(data?.error || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      setError(err.message || 'Unable to connect to the prediction server. Please try again.');
      setIsConnected(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError('');
  };

  return (
    <div className="app-container">
      <div className="bg-glow"></div>
      <div className="main-content">
        <Header isConnected={isConnected} />

        <main className="dashboard-grid">
          <PredictionForm
            onPredict={handlePredict}
            isLoading={isLoading}
            externalError={error}
            setExternalError={setError}
          />

          {result && (
            <PredictionResult
              result={result}
              onReset={handleReset}
            />
          )}
        </main>

        <footer className="app-footer">
          <p>Powered by Flask REST API & Trained Scikit-Learn Model</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
