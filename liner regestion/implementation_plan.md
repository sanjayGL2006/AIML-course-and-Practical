# Implementation Plan - Production-Ready Height-to-Weight ML Prediction Web App

Create a full-stack production-ready machine learning web application using **React (Vite)** on the frontend and **Flask REST API** on the backend, powered by a trained Linear Regression Machine Learning model (`height_weight_model.pk`).

## User Review Required

> [!IMPORTANT]
> - **Model File (`height_weight_model.pk`)**: The workspace was initially empty. We will generate and serialize a reference `scikit-learn` `LinearRegression` model to `backend/model/height_weight_model.pk` trained on standard Height (cm) to Weight (kg) data (e.g. 170 cm yields ~65.4 kg).
> - **Backend & Frontend Separation**: Strict separation between Vite React UI and Flask Python REST API communicating via Axios over JSON endpoints with CORS enabled.

## Proposed Changes

### Model & Scripting

#### [NEW] [generate_model.py](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/generate_model.py)
- Script to generate and save `height_weight_model.pk` into `backend/model/` using `joblib` / `pickle` with `scikit-learn` `LinearRegression`.

---

### Backend Component (`backend/`)

#### [NEW] [backend/app.py](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/app.py)
- Flask application initializing CORS and loading `height_weight_model.pk` once on start.
- `GET /api/health` returning `{"status": "success", "message": "API is running"}`.
- `POST /api/predict` parsing JSON `{"height": number}`, validating bounds (50–250 cm, numeric, > 0), predicting via `model.predict([[height]])`, and returning `{"success": true, "height": 170, "predicted_weight": 65.42}`.
- Error handling for invalid input (400), model missing/failure (500), and generic server errors without leaking stack traces.

#### [NEW] [backend/requirements.txt](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/requirements.txt)
- Dependencies: `Flask`, `Flask-CORS`, `python-dotenv`, `joblib`, `scikit-learn`, `gunicorn`, `pytest`.

#### [NEW] [backend/.env.example](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/.env.example) and [backend/.env](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/.env)
- Environment variables: `FLASK_ENV=development`, `PORT=5000`, `FRONTEND_URL=http://localhost:5173`.

#### [NEW] [backend/tests/test_api.py](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/tests/test_api.py)
- pytest test suite testing health check, valid prediction (170cm), missing height, string height, zero height, negative height, and out-of-range height.

#### [NEW] [backend/README.md](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/backend/README.md)
- Backend installation, virtualenv creation, API endpoints documentation, running dev server, and Gunicorn WSGI production deployment commands.

---

### Frontend Component (`frontend/`)

#### [NEW] Vite React App Setup
- Scaffolding frontend app with Vite React template.

#### [NEW] [frontend/src/services/api.js](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/services/api.js)
- Axios client configured with `VITE_API_URL` environment variable for `checkHealth` and `predictWeight`.

#### [NEW] [frontend/src/components/Header.jsx](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/components/Header.jsx)
- Sleek hero header displaying "Height → Weight Predictor" title, subtitle, AI badge, and live server status indicator.

#### [NEW] [frontend/src/components/PredictionForm.jsx](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/components/PredictionForm.jsx)
- Form component with number input `Height (cm)`, range validation (50 - 250 cm), clear error prompts, quick height presets (e.g., 160cm, 170cm, 180cm), and animated loading button state ("Predicting...").

#### [NEW] [frontend/src/components/PredictionResult.jsx](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/components/PredictionResult.jsx)
- Modern result view featuring large weight badge in `kg`, comparison summary, input height echo, and notice confirming model execution.

#### [NEW] [frontend/src/App.jsx](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/App.jsx)
- Main view composing `Header`, `PredictionForm`, and `PredictionResult` with global error handling, reset functionality, and responsive card container.

#### [NEW] [frontend/src/index.css](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/src/index.css)
- Premium dark-theme design system: modern typography, glassmorphism cards, glowing gradients, smooth micro-interactions, responsive grids.

#### [NEW] [frontend/.env](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/.env) and [frontend/.env.example](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/frontend/.env.example)
- Environment variable configuration: `VITE_API_URL=http://127.0.0.1:5000`.

---

### Root Configuration

#### [NEW] [.gitignore](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/.gitignore)
- Standard git ignore file for Python (`__pycache__`, `venv`), Node (`node_modules`, `dist`), and env secrets.

#### [NEW] [README.md](file:///c:/Users/Sanjay%20G%20L/Desktop/liner%20regestion/README.md)
- Root documentation covering overview, architecture flow diagram, tech stack, quick start guide, API specification, testing guide, and production setup (Gunicorn + Vite build).

---

## Verification Plan

### Automated Tests
- Run backend pytest suite:
  ```bash
  cd backend
  python -m pytest tests/
  ```

### Manual Verification
1. Start Flask API server on port 5000 (`python backend/app.py`).
2. Start React Vite dev server on port 5173 (`npm run dev --prefix frontend`).
3. Verify health status (`http://127.0.0.1:5000/api/health`).
4. Test frontend UI in browser:
   - Valid entry `170`: expect ~`65.42 kg`.
   - Empty height: expect `"Please enter your height."` validation error.
   - Invalid height string/out-of-range (`300` or `-5`): expect `"Please enter a height between 50 cm and 250 cm."`.
   - Verify network call goes to Flask `/api/predict` and prediction matches.
