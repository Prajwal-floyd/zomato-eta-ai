import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2


# ---------------------------------------------------
# DISTANCE FEATURE
# ---------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def create_distance_feature(df):

    df['distance_km'] = df.apply(

        lambda row: haversine(

            row['Restaurant_latitude'],
            row['Restaurant_longitude'],

            row['Delivery_location_latitude'],
            row['Delivery_location_longitude']

        ),

        axis=1
    )

    return df


# ---------------------------------------------------
# TIME FEATURES
# ---------------------------------------------------

def create_time_features(df):

    ordered_time = pd.to_datetime(

        df['Time_Orderd']
        .astype(str)
        .str.strip(),

        

        errors='coerce'
    )

    df['order_hour'] = ordered_time.dt.hour

    df['is_rush_hour'] = df['order_hour'].apply(

        lambda x: 1 if x in [12, 13, 19, 20, 21] else 0

    )

    return df


# ---------------------------------------------------
# PREP TIME FEATURE
# ---------------------------------------------------
def normalize_time(val):

    try:

        val = str(val).strip()

        # Handle Excel decimal-style times
        if '.' in val and ':' not in val:

            excel_time = float(val)

            total_seconds = int(
                excel_time * 24 * 60 * 60
            )

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            return f"{hours:02d}:{minutes:02d}"

        return val

    except:

        return np.nan


def create_prep_time_feature(df):

    ordered_clean = (
        df['Time_Orderd']
        .apply(normalize_time)
    )

    picked_clean = (
        df['Time_Order_picked']
        .apply(normalize_time)
    )

    ordered_time = pd.to_datetime(
        ordered_clean,
        format='%H:%M',
        errors='coerce'
    )

    picked_time = pd.to_datetime(
        picked_clean,
        format='%H:%M',
        errors='coerce'
    )

    prep_time = (
        picked_time - ordered_time
    ).dt.total_seconds() / 60

    prep_time = prep_time.apply(

        lambda x:
        x + 1440
        if pd.notnull(x) and x < 0
        else x

    )

    df['prep_time'] = prep_time

    return df


# ---------------------------------------------------
# TRAFFIC FEATURE
# ---------------------------------------------------

def create_traffic_feature(df):

    traffic_map = {

        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Jam': 4

    }

    df['traffic_score'] = (

        df['Road_traffic_density']
        .astype(str)
        .str.strip()
        .map(traffic_map)

    )

    return df


# ---------------------------------------------------
# WEATHER FEATURE
# ---------------------------------------------------

def create_weather_feature(df):

    weather_map = {

        'Sunny': 1,
        'Cloudy': 2,
        'Fog': 3,
        'Stormy': 4,
        'Sandstorms': 4,
        'Windy': 2

    }

    df['weather_score'] = (

        df['Weather_conditions']
        .astype(str)
        .str.strip()
        .map(weather_map)

    )

    return df
# ---------------------------------------------------
# TRAFFIC DISTANCE INTERACTION
# ---------------------------------------------------

def create_interaction_feature(df):

    df['traffic_distance'] = (
        df['traffic_score'] *
        df['distance_km']
    )

    return df


# ---------------------------------------------------
# WEEKEND FEATURE
# ---------------------------------------------------

def create_weekend_feature(df):

    df['Order_Date'] = pd.to_datetime(
        df['Order_Date'],
        errors='coerce'
    )

    df['is_weekend'] = (
        df['Order_Date']
        .dt.dayofweek
        .apply(lambda x: 1 if x >= 5 else 0)
    )

    return df


# ---------------------------------------------------
# CITY AVG ETA FEATURE
# ---------------------------------------------------

def create_city_eta_feature(df):

    df['city_avg_eta'] = (

        df.groupby('City')[
            'Time_taken (min)'
        ].transform('mean')

    )

    return df