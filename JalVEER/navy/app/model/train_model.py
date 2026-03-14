import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
scenarios_df = pd.read_csv("../data/naval_conflict_scenarios_700.csv")

# Features
features = [
    'att_avg_threat',
    'att_avg_tech_gen',
    'att_avg_stealth',
    'att_avg_ew',
    'att_fighter_count',
    'att_military_budget',
    'dfn_avg_threat',
    'dfn_avg_tech_gen',
    'dfn_avg_stealth',
    'dfn_avg_ew',
    'dfn_fighter_count',
    'dfn_military_budget'
]

X = scenarios_df[features]
y = scenarios_df['outcome']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "war_model.pkl")

print("Model saved successfully!")