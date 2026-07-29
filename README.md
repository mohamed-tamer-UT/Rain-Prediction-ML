# 🌧️ Rain Prediction ML

A complete Machine Learning project developed during the **NTI Creativa Innovation Hub Program (Benha Branch)**.

This project predicts whether it will rain tomorrow using historical Australian weather data. The project covers the entire machine learning workflow starting from data preprocessing and exploratory data analysis (EDA), through feature engineering, model training, evaluation, model deployment using Streamlit, and complete project documentation.

---

# 📌 Project Overview

Predicting rainfall is one of the most important weather forecasting tasks because it helps support agriculture, transportation, water resource management, and disaster prevention.

In this project, several Machine Learning algorithms were trained and compared to determine the best model for rainfall prediction.

The final model was deployed using **Streamlit** to provide an easy-to-use interactive web application.

---

# 🎯 Project Objectives

- Clean and preprocess raw weather data.
- Perform Exploratory Data Analysis (EDA).
- Engineer meaningful features.
- Train multiple Machine Learning models.
- Compare model performance.
- Select the best model.
- Save the trained model using Pickle.
- Build an interactive Streamlit application.
- Deploy the project for inference.

---

# 📂 Dataset

**Dataset Name**

WeatherAUS Dataset

**Target Variable**

RainTomorrow

- Yes
- No

The dataset contains historical Australian weather observations including:

- Temperature
- Humidity
- Atmospheric Pressure
- Sunshine
- Wind Speed
- Rainfall
- Cloud Cover
- Evaporation
- Wind Direction
- and many additional weather attributes.

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Streamlit
- Pickle
- JSON

---

# ⚙ Machine Learning Pipeline

The project follows a complete ML workflow:

## 1. Data Cleaning

- Removed duplicated records.
- Handled missing values.
- Removed invalid observations.
- Fixed inconsistent values.

---

## 2. Feature Engineering

Several new features were created including:

- Pressure Difference
- Temperature Difference
- Wind Speed Categories
- Humidity Indicators

These engineered features improved the predictive performance of the models.

---

## 3. Data Preprocessing

- Numerical feature scaling
- Categorical encoding
- Column Transformer pipeline
- Pipeline integration

---

## 4. Model Training

Multiple models were trained and compared including:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost (if available)
- Other classification models

---

## 5. Model Evaluation

Models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix
- ROC Curve

The best-performing model was selected and saved.

---

# 📊 Feature Importance

Feature importance analysis showed that the most influential variables include:

1. Humidity at 3 PM
2. Pressure at 3 PM
3. Wind Gust Speed
4. Pressure Difference
5. Sunshine

These weather conditions contributed the most to predicting rainfall.

---

# 💾 Saved Model

The final trained model is stored as:

```
rain_prediction_model.pkl
```

Additional preprocessing metadata is stored in:

```
model_meta.json
```

---

# 🖥 Streamlit Application

The trained model was deployed using **Streamlit**.

The application allows users to:

- Enter weather measurements.
- Predict whether it will rain tomorrow.
- Display prediction results instantly.

---

# 📸 Application Preview

## Home Page

![Home](home.png)

---

## Prediction Result

![Prediction](prediction.png)

---

# 📁 Repository Structure

```
Rain-Prediction-ML
│
├── app.py
├── rain_prediction_model.pkl
├── model_meta.json
├── requirements.txt
├── RainPrediction_Documentation.pdf
├── WEATHERAUS_FINAL_updated.ipynb
├── home.png
├── prediction.png
└── README.md
```

---

# ▶ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Rain-Prediction-ML.git
```

Move into the project directory

```bash
cd Rain-Prediction-ML
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run app.py
```

---

# 📈 Results

The selected model achieved strong predictive performance after:

- Data Cleaning
- Feature Engineering
- Hyperparameter Tuning
- Model Comparison

The deployment provides real-time inference through an interactive user interface.

---

# 🔮 Future Improvements

Possible future enhancements include:

- Cloud deployment
- Docker containerization
- API development using FastAPI
- Continuous model retraining
- Real-time weather API integration
- Advanced ensemble techniques

---

# 👨‍💻 Author

**Mohamed Tamer**

NTI Creativa Innovation Hub Program

Benha Branch

Machine Learning Track

---

# 📄 Documentation

The complete project documentation is included in:

```
RainPrediction_Documentation.pdf
```

---

# ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---

# 🌧️ Rain Prediction ML

A complete Machine Learning project developed during the NTI Creativa Innovation Hub Program.

## 🚀 Live Demo

---

## 📂 Dataset

This project is built using the **WeatherAUS** dataset.

**Dataset Source:**
https://www.kaggle.com/datasets/trisha2094/weatheraus

The dataset contains historical daily weather observations collected from multiple weather stations across Australia and is used to predict whether it will rain on the following day (`RainTomorrow`). :contentReference[oaicite:0]{index=0}
👉 **Live Application**

https://rain-prediction-ml-w4kov8lxpkvufsad3pnymf.streamlit.app/

---
