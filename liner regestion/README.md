# Height-to-Weight Machine Learning Prediction Application

A production-ready Machine Learning web application that predicts **weight (kg)** from **height (cm)** using a pre-trained scikit-learn model (`height_weight_model.pk`).

---

## 🌟 Architecture Overview

```text
User
  ↓
React Frontend (Vite)
  ↓ [Input: Height in cm]
Click "Predict Weight"
  ↓
POST /api/predict
  ↓
Flask REST API Backend
  ↓
Load & execute height_weight_model.pk
  ↓ model.predict([[height]])
Predicted Weight (kg)
  ↓
JSON Response
  ↓
React Frontend Dashboard
  ↓ [Output Display: Weight in kg]
```

---

## 🚀 Tech Stack

### Frontend
- **Framework**: React.js (Vite template)
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Styling**: Vanilla CSS (Glassmorphism dark theme, custom utility classes, responsive grid layout)

### Backend
- **Framework**: Python Flask
- **CORS**: Flask-CORS
- **Model Loader**: `joblib` / `pickle`
- **Testing**: `pytest`
- **WSGI**: Gunicorn (Linux) / Waitress (Windows)

### Machine Learning Model
- **File**: `height_weight_model.pk` (stored in `backend/model/`)
- **Algorithm**: Linear Regression (`scikit-learn`)
- **Input**: Height in cm (numeric)
- **Output**: Predicted Weight in kg (numeric)

---

## 📁 Project Structure

```text
height-weight-prediction/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # Title, badge, and live server status indicator
│   │   │   ├── PredictionForm.jsx  # Input form, validation, loading spinner & presets
│   │   │   └── PredictionResult.jsx# Display card for returned weight prediction
│   │   │
│   │   ├── services/
│   │   │   └── api.js              # Axios API service module
│   │   │
│   │   ├── App.jsx                 # Application layout and global state manager
│   │   ├── main.jsx                # React DOM entrypoint
│   │   └── index.css               # Design system & dark theme stylesheet
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env
│
├── backend/
│   ├── app.py                      # Flask REST API server
│   ├── model/
│   │   └── height_weight_model.pk  # Trained ML model file
│   │
│   ├── tests/
│   │   └── test_api.py             # Pytest automated test suite
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment configuration
│   └── README.md                   # Backend documentation
│
├── generate_model.py               # Model generation script
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start Guide

### 1. Start the Flask Backend

```bash
# Move to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```
> Server runs at: `http://localhost:5000`

### 2. Start the React Frontend

Open a new terminal window:

```bash
# Move to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
> Web application opens at: `http://localhost:5173`

---

## 🧪 Testing

### Backend Unit Tests
Run backend tests with `pytest`:

```bash
python -m pytest backend/tests/test_api.py
```

### Manual E2E Validation
1. Open `http://localhost:5173` in your browser.
2. Enter `170` into the Height input field.
3. Click **Predict Weight**.
4. Verify the backend `/api/predict` endpoint is called.
5. Verify the model prediction returns `65.42 kg` and displays prominently on screen.

---

## 🔒 Security & Input Validation

- **Format Validation**: Ensures height is a valid numeric value.
- **Range Boundaries**: Restricts height input to valid range (50 cm – 250 cm).
- **Error Privacy**: Prevents exposure of internal Python tracebacks to clients in production mode.
- **CORS Configured**: Restricted to authorized frontend origins.
- **Single Model Load**: Model file `height_weight_model.pk` is loaded once into memory during Flask startup for performance efficiency.

---

## 🌐 Production Deployment

### Building Frontend
```bash
cd frontend
npm run build
```

### Running Production Backend Server
```bash
cd backend
gunicorn --bind 0.0.0.0:5000 app:app --workers 4
```
