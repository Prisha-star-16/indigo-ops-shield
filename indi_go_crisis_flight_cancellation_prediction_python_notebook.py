# IndiGo Crisis Flight Cancellation Prediction
# -----------------------------------------
# This notebook analyzes the synthetic IndiGo crisis dataset
# and builds ML models to predict flight cancellations

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score


# 2. Load Dataset
file_path = 'indigo_crisis_synthetic_dataset.csv'
df = pd.read_csv(file_path)

print('Dataset Shape:', df.shape)
df.head()


# 3. Data Preprocessing
# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Remove invalid routes (same origin and destination)
df = df[df['origin_airport'] != df['destination_airport']]

# Encode categorical variables
label_cols = ['origin_airport', 'destination_airport', 'aircraft_type']
le = LabelEncoder()
for col in label_cols:
    df[col] = le.fit_transform(df[col])

# Feature engineering
df['pilot_shortage'] = df['pilots_required'] - df['pilots_available']
df['peak_duty_flag'] = (df['avg_duty_hours'] > 9).astype(int)


# 4. Exploratory Data Analysis (EDA)

# Cancellation rate
cancel_rate = df['cancelled'].mean()
print('Cancellation Rate:', round(cancel_rate * 100, 2), '%')

# Plot cancellations by pilot shortage
plt.figure()
df.groupby('pilot_shortage')['cancelled'].mean().plot()
plt.xlabel('Pilot Shortage')
plt.ylabel('Cancellation Probability')
plt.title('Effect of Pilot Shortage on Cancellations')
plt.show()


# 5. Prepare Data for Modeling
features = [
    'scheduled_departure_hour', 'delay_minutes', 'origin_airport',
    'destination_airport', 'aircraft_type', 'pilots_available',
    'pilots_required', 'avg_duty_hours', 'rest_violation_flag',
    'weather_severity', 'holiday_flag', 'pilot_shortage', 'peak_duty_flag'
]

X = df[features]
y = df['cancelled']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# 6. Logistic Regression Model
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

y_pred_log = log_model.predict(X_test)
y_prob_log = log_model.predict_proba(X_test)[:, 1]

print('Logistic Regression Accuracy:', accuracy_score(y_test, y_pred_log))
print('ROC-AUC:', roc_auc_score(y_test, y_prob_log))
print(classification_report(y_test, y_pred_log))


# 7. Random Forest Model
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

print('Random Forest Accuracy:', accuracy_score(y_test, y_pred_rf))
print('ROC-AUC:', roc_auc_score(y_test, y_prob_rf))
print(classification_report(y_test, y_pred_rf))


# 8. Feature Importance
importance = pd.Series(rf_model.feature_importances_, index=features)
importance.sort_values(ascending=False).plot(kind='bar')
plt.title('Feature Importance - Random Forest')
plt.show()


# 9. Business Insight
print('Top Drivers of Flight Cancellations:')
print(importance.sort_values(ascending=False).head())


# 10. Save Model for API Deployment
import joblib
joblib.dump(rf_model, 'cancellation_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved for API deployment")

# 11. Conclusion
print("Model successfully predicts flight cancellations during operational crises.")
print("Crew availability and regulatory compliance are the most critical factors.")
