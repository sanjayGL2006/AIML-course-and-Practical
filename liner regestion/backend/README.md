# Height-to-Weight Prediction - Backend REST API

This is the Python Flask REST API backend for the Height-to-Weight Machine Learning Prediction service. It loads the pre-trained `height_weight_model.pk` model file into memory once on startup and serves JSON prediction requests.

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **Flask** (REST Framework)
- **Flask-CORS** (Cross-Origin Resource Sharing)
- **joblib / pickle** (Model Deserialization)
- **scikit-learn** (Machine Learning Model Pipeline)
- **pytest** (Automated Unit Testing)
- **gunicorn / waitress** (WSGI Server for Production)

---

## 📁 Folder Structure

```text
backend/
├── app.py                  # Main Flask REST API application
├── model/
│   └── height_weight_model.pk # Pre-trained ML model file
├── tests/
│   └── test_api.py         # Pytest test suite
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables (ignored by git)
├── .env.example            # Environment variables template
└── README.md               # Backend documentation
```

---

## 🚀 Setup & Local Development

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

Activate virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file based on `.env.example`:

```ini
FLASK_ENV=development
PORT=5000
FRONTEND_URL=http://localhost:5173
```

### 4. Run Development Server

```bash
python app.py
```

Server will start on `http://127.0.0.1:5000`.

---

## 🧪 Testing

Run backend tests using `pytest`:

```bash
python -m pytest tests/test_api.py
```

---

## 📡 API Specification

### Health Check

```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "API is running"
}
```

### Predict Weight

```http
POST /api/predict
Content-Type: application/json

{
  "height": 170
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "height": 170.0,
  "predicted_weight": 65.42
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Please enter a height between 50 cm and 250 cm."
}
```

---

## 🌐 Production WSGI Deployment

For production deployments, run Flask using Gunicorn (Linux) or Waitress (Windows):

### Linux / Production Server with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 app:app --workers 4
```

### Windows Production Deployment with Waitress:
```bash
pip install waitress
waitress-serve --port=5000 app:app
```
