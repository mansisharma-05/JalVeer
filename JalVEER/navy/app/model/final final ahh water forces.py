import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

countries_df = pd.read_csv("../data/naval_countries_profiles.csv")
systems_df = pd.read_csv("../data/navy_systems_enhanced_82.csv")
scenarios_df = pd.read_csv("../data/naval_conflict_scenarios_700.csv")
 
countries_df.head()
systems_df.head()
scenarios_df.head()

countries_df.info()
systems_df.info()
scenarios_df.info()

countries_df.isnull().sum()
systems_df.isnull().sum()
scenarios_df.isnull().sum()

countries_df = countries_df.drop_duplicates()
systems_df = systems_df.drop_duplicates()
scenarios_df = scenarios_df.drop_duplicates()

countries_df = countries_df.fillna(0)
systems_df = systems_df.fillna(0)
scenarios_df = scenarios_df.fillna(0)

print("Countries DF columns:")
print(countries_df.columns)

print("\nSystems DF columns:")
print(systems_df.columns)

merged_df = pd.merge(countries_df, systems_df, on="country", how="inner")

print(merged_df.shape)
merged_df.head()

tech_columns = [
    "tech_generation",
    "stealth_rating",
    "ew_capability",
    "max_speed_kmph",
    "range_km",
    "reliability",
    "threat_level"
]

tech_df = merged_df[tech_columns]

tech_df.head()

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

tech_scaled = scaler.fit_transform(tech_df)

tech_scaled = pd.DataFrame(tech_scaled, columns=tech_columns)

tech_scaled.head()

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42)

kmeans.fit(tech_scaled)

clusters = kmeans.labels_

merged_df["Technology_Cluster"] = clusters

merged_df[["country", "Technology_Cluster"]].head()

merged_df["Technology_Cluster"].value_counts()

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=tech_scaled["tech_generation"],
    y=tech_scaled["stealth_rating"],
    hue=merged_df["Technology_Cluster"],
    palette="Set1"
)

plt.title("Technology Clusters of Naval Systems")
plt.show()

merged_df + scenarios_df

final_df = pd.merge(merged_df, scenarios_df, on="country", how="inner")

print(final_df.shape)
final_df.head()


print("\nScenario Dataset Columns:")
print(scenarios_df.columns)


possible_cols = ['incident_type','event_type','engagement','scenario_type',
                 'conflict_type','interaction_type','action','activity']

event_col = None
for col in possible_cols:
    if col in scenarios_df.columns:
        event_col = col
        break



print("\nUsing column for conflict detection:", event_col)


war_keywords = [
    'missile', 'strike', 'attack', 'battle', 'combat',
    'torpedo', 'armed', 'engagement', 'blockade',
    'shelling', 'skirmish', 'submarine attack',
    'naval battle', 'invasion'
]


def create_war_label(value):
    if pd.isna(value):
        return 0
    value = str(value).lower()

    for word in war_keywords:
        if word in value:
            return 1
    return 0


scenarios_df['conflict_occurred'] = scenarios_df[event_col].apply(create_war_label)


print("\nTarget Variable Distribution:")
print(scenarios_df['conflict_occurred'].value_counts())


print("\nSample labelled data:")
print(scenarios_df[[event_col,'conflict_occurred']].head(10))

def assign_zone(country):
    indo_pacific = ['India','China','Japan','Australia']
    nato = ['USA','UK','France','Germany','Italy']
    middle_east = ['Iran','Saudi Arabia','Israel']
    east_asia = ['North Korea','South Korea','Taiwan']

    if country in indo_pacific:
        return 'IndoPacific'
    elif country in nato:
        return 'NATO'
    elif country in middle_east:
        return 'MiddleEast'
    elif country in east_asia:
        return 'EastAsia'
    else:
        return 'Other'

final_df['zone'] = final_df['country'].apply(assign_zone)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
final_df['zone'] = le.fit_transform(final_df['zone'])

features = [
    'naval_budget',
    'fleet_size',
    'gdp',
    'threat_level',
    'Technology_Cluster',
    'zone',
    'past_conflicts',
    'tension_index'
]

X = final_df[features]
y = final_df['conflict_occurred']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

prob = rf_model.predict_proba(X_test)

print(prob[:10])

import joblib
joblib.dump(rf_model, "war_prediction_model.pkl")

joblib.dump(scaler, "scaler.pkl")


