import pandas as pd
import joblib

from lightgbm import LGBMRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

from src.features import (
    create_distance_feature,
    create_time_features,
    create_prep_time_feature,
    create_traffic_feature,
    create_weather_feature
)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("data/train.csv")


# ---------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------

df.columns = df.columns.str.strip()


# ---------------------------------------------------
# CLEAN TARGET COLUMN
# ---------------------------------------------------

df['Time_taken (min)'] = (
    df['Time_taken (min)']
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(float)
)


# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

df = create_distance_feature(df)

df = create_time_features(df)

df = create_prep_time_feature(df)

df = create_traffic_feature(df)

df = create_weather_feature(df)


# ---------------------------------------------------
# CLEAN NUMERIC COLUMNS
# ---------------------------------------------------

df['Delivery_person_Age'] = pd.to_numeric(
    df['Delivery_person_Age'],
    errors='coerce'
)

df['Delivery_person_Ratings'] = pd.to_numeric(
    df['Delivery_person_Ratings'],
    errors='coerce'
)

df['multiple_deliveries'] = pd.to_numeric(
    df['multiple_deliveries'],
    errors='coerce'
)


# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------

df = df.ffill()


# ---------------------------------------------------
# ENCODE CATEGORICAL FEATURES
# ---------------------------------------------------

categorical_cols = [
    'Weather_conditions',
    'Road_traffic_density',
    'Type_of_order',
    'Type_of_vehicle',
    'Festival',
    'City'
]

le = LabelEncoder()

for col in categorical_cols:

    df[col] = le.fit_transform(
        df[col].astype(str)
    )


# ---------------------------------------------------
# FEATURE LIST
# ---------------------------------------------------

features = [

    'Delivery_person_Age',

    'Delivery_person_Ratings',

    'Vehicle_condition',

    'multiple_deliveries',

    'Weather_conditions',

    'Road_traffic_density',

    'Type_of_order',

    'Type_of_vehicle',

    'Festival',

    'City',

    'distance_km',

    'order_hour',

    'is_rush_hour',

    'prep_time',

    'traffic_score',

    'weather_score'
]


# ---------------------------------------------------
# INPUTS & TARGET
# ---------------------------------------------------

X = df[features]

y = df['Time_taken (min)']


# ---------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ---------------------------------------------------
# MODEL
# ---------------------------------------------------

model = LGBMRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=10,
    random_state=42
)


# ---------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------

model.fit(X_train, y_train)


# ---------------------------------------------------
# PREDICTIONS
# ---------------------------------------------------

preds = model.predict(X_test)


# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------

mae = mean_absolute_error(y_test, preds)

r2 = r2_score(y_test, preds)

print(f"\nMAE: {mae:.2f}")

print(f"R2 Score: {r2:.2f}")


# ---------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------

importance_df = pd.DataFrame({

    'Feature': X.columns,

    'Importance': model.feature_importances_

})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

print("\nFeature Importance:\n")

print(importance_df)


# ---------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------

joblib.dump(
    model,
    "models/lgbm_model.pkl"
)

print("\nModel saved successfully!")