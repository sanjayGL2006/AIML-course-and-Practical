import React, { useState } from 'react';
import { Ruler, Loader2, Sparkles, AlertCircle } from 'lucide-react';

const PredictionForm = ({ onPredict, isLoading, externalError, setExternalError }) => {
  const [height, setHeight] = useState('');
  const [localError, setLocalError] = useState('');

  const validateInput = (value) => {
    if (value === '' || value === null || value === undefined) {
      return 'Please enter your height.';
    }
    const num = Number(value);
    if (isNaN(num)) {
      return 'Please enter a valid height.';
    }
    if (num <= 0) {
      return 'Please enter a valid height.';
    }
    if (num < 50 || num > 250) {
      return 'Please enter a height between 50 cm and 250 cm.';
    }
    return '';
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setHeight(val);
    setLocalError('');
    if (setExternalError) setExternalError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errorMsg = validateInput(height);
    if (errorMsg) {
      setLocalError(errorMsg);
      return;
    }
    setLocalError('');
    onPredict(Number(height));
  };

  const handleQuickPreset = (presetValue) => {
    setHeight(presetValue.toString());
    setLocalError('');
    if (setExternalError) setExternalError('');
    onPredict(presetValue);
  };

  const displayError = localError || externalError;

  return (
    <div className="card form-card">
      <div className="card-header">
        <div className="icon-badge">
          <Ruler className="icon-md text-emerald-400" />
        </div>
        <h2>Enter Your Height</h2>
      </div>

      <form onSubmit={handleSubmit} className="prediction-form" noValidate>
        <div className="form-group">
          <label htmlFor="height-input" className="form-label">
            Height (cm)
          </label>
          <div className="input-wrapper">
            <input
              id="height-input"
              type="number"
              step="any"
              placeholder="e.g. 170"
              value={height}
              onChange={handleInputChange}
              disabled={isLoading}
              className={`form-input ${displayError ? 'input-error' : ''}`}
              min="50"
              max="250"
            />
            <span className="unit-tag">cm</span>
          </div>
          <span className="input-hint">Allowed range: 50 cm – 250 cm</span>
        </div>

        {displayError && (
          <div className="error-box">
            <AlertCircle className="icon-sm text-rose-400 shrink-0" />
            <span>{displayError}</span>
          </div>
        )}

        <div className="quick-presets">
          <span className="preset-label">Quick select:</span>
          {[160, 170, 180, 190].map((preset) => (
            <button
              key={preset}
              type="button"
              className="preset-btn"
              onClick={() => handleQuickPreset(preset)}
              disabled={isLoading}
            >
              {preset} cm
            </button>
          ))}
        </div>

        <button
          id="predict-submit-btn"
          type="submit"
          disabled={isLoading}
          className="submit-btn"
        >
          {isLoading ? (
            <>
              <Loader2 className="spinner icon-sm" />
              <span>Predicting...</span>
            </>
          ) : (
            <>
              <Sparkles className="icon-sm" />
              <span>Predict Weight</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default PredictionForm;
