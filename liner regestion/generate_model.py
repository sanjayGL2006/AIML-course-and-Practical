import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_and_save_model():
    # Generate realistic sample data for Height (cm) -> Weight (kg)
    # Target: 170 cm yields ~65.42 kg
    # Slope ~ 0.707, Intercept ~ -54.77
    np.random.seed(42)
    heights = np.linspace(140, 210, 100).reshape(-1, 1)
    
    # y = 0.7074 * height - 54.838
    # For 170cm: 0.7074 * 170 - 54.838 = 120.258 - 54.838 = 65.42 kg
    slope = 0.7074
    intercept = -54.838
    weights = (slope * heights + intercept).ravel()
    
    # Fit Linear Regression Model
    model = LinearRegression()
    model.fit(heights, weights)
    
    # Test prediction for 170 cm
    test_pred = model.predict([[170]])[0]
    print(f"Model trained successfully. Test prediction for 170 cm: {test_pred:.2f} kg")
    
    # Ensure backend/model directory exists
    target_dir = os.path.join(os.path.dirname(__file__), "backend", "model")
    os.makedirs(target_dir, exist_ok=True)
    
    model_path = os.path.join(target_dir, "height_weight_model.pk")
    joblib.dump(model, model_path)
    print(f"Saved trained model to: {os.path.abspath(model_path)}")
    
    # Also save a copy in root if needed
    root_model_path = os.path.join(os.path.dirname(__file__), "height_weight_model.pk")
    joblib.dump(model, root_model_path)
    print(f"Saved copy to root: {os.path.abspath(root_model_path)}")

if __name__ == "__main__":
    generate_and_save_model()
