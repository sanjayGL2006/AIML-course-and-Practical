import React from 'react';
import { Activity, Cpu, CheckCircle, AlertCircle } from 'lucide-react';

const Header = ({ isConnected }) => {
  return (
    <header className="header-container">
      <div className="badge-wrapper">
        <span className="badge">
          <Cpu className="icon-sm text-cyan-400" />
          <span>Production ML Engine</span>
        </span>
        <div className={`status-indicator ${isConnected ? 'status-online' : 'status-offline'}`}>
          <span className="status-dot"></span>
          <span className="status-text">{isConnected ? 'Server Online' : 'Server Offline'}</span>
        </div>
      </div>
      
      <h1 className="title-gradient">
        Height <span className="arrow-accent">→</span> Weight Predictor
      </h1>
      
      <p className="subtitle">
        Predict weight using a trained Machine Learning model
      </p>
    </header>
  );
};

export default Header;
