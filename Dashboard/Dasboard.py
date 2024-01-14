import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='date_time').agg({
        'total_count_hourly' : 'sum'
    }).reset_index()

    return daily_rent_df

def create_hourly_rent_df(df): 
    hourly_rent_df = df.groupby(['hour', 'season_hourly', 'weather_condition_hourly']).agg(
        avg_count_hourly=('total_count_hourly' , 'mean'),
        sum_count_hourly=('total_count_hourly' , 'sum')
    ).reset_index() 

    return hourly_rent_df

def create_weekday_rent_df(df): 
    weekday_rent_df = df.groupby(['weekday_hourly', 'season_hourly', 'weather_condition_hourly']).agg(
        avg_count_weekday=('total_count_hourly' , 'mean'),
        sum_count_weekday=('total_count_hourly' , 'sum')
    ).reset_index() 
    weekday_rent_df['weekday_hourly']=pd.Categorical(weekday_rent_df['weekday_hourly'], ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])

    return weekday_rent_df

def create_daily_rent_casual(df):
    daily_rent_casual = df.resample(rule='D', on='date_time').agg({
        'casual_hourly' : 'sum'
    }).reset_index()

    return daily_rent_casual

def create_daily_rent_registered(df):
    daily_rent_registered = df.resample(rule='D', on='date_time').agg({
        'registered_hourly' : 'sum'
    }).reset_index()

    return daily_rent_registered

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(['month_hourly', 'season_hourly', 'weather_condition_hourly']).agg(
        avg_count_month=('total_count_hourly' , 'mean'),
        sum_count_month=('total_count_hourly' , 'sum')
    ).reset_index()
    monthly_rent_df['month_hourly'] = pd.Categorical(monthly_rent_df['month_hourly'], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    return monthly_rent_df

def create_holiday_df(df): 
    rent_holiday_df=df.groupby('holiday_hourly').total_count_hourly.mean().reset_index()
    return rent_holiday_df

def create_temp_df(df) : 
    temp_df = df.groupby(['date_time', 'temp_hourly', 'season_hourly']).total_count_hourly.mean().reset_index()

    return temp_df


all_df = pd.read_csv("all_data_bike_sharing.csv")

datetime_columns = ["date_time"]
all_df.sort_values(by="date_time", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df["date_time"].min()
max_date = all_df["date_time"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn3.vectorstock.com/i/1000x1000/37/87/bicycle-sharing-system-rgb-color-icon-vector-35393787.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date_time"] >= str(start_date)) & 
                (all_df["date_time"] <= str(end_date))]

hourly_rent_df = create_hourly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
daily_rent_df = create_daily_rent_df(main_df)
daily_rent_casual = create_daily_rent_casual(main_df)
daily_rent_registered = create_daily_rent_registered(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
holiday_df = create_holiday_df(main_df)
temp_df = create_temp_df(main_df)

with st.sidebar : 
    temp_count_min = round(temp_df.temp_hourly.min())
    temp_count_max = round(temp_df.temp_hourly.max())
    st.metric(label="Min Temperature", value=temp_count_min)
    st.metric(label="Max Temperature", value=temp_count_max)


st.title('Bike Sharing System on 2011-2012')

# Performa Perjam 
st.header('Hourly Rents')

total_rents_hourly = round(hourly_rent_df.avg_count_hourly.sum())
st.metric("Total bike rents", value=total_rents_hourly)

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x=hourly_rent_df["hour"],
    y=hourly_rent_df["avg_count_hourly"],
    marker='o', 
    linewidth=2,
    color="#90CAF9",
    errorbar=None,
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# Performa Perjam Berdasarkan Season
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=hourly_rent_df["hour"],
    y=hourly_rent_df["avg_count_hourly"],
    hue=hourly_rent_df['season_hourly'],
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Relation Season vs Hourly Rents", loc='center', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# Performa Perjam Berdasarkan Weather Condition
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=hourly_rent_df["hour"],
    y=hourly_rent_df["avg_count_hourly"],
    hue=hourly_rent_df['weather_condition_hourly'],
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Relation Weather Condition vs Hourly Rents", loc='center', fontsize=25)
ax.legend(loc='upper right')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

#Performa Harian 
st.header('Daily Rents')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rents = round(daily_rent_df.total_count_hourly.sum())
    st.metric("Total bike rents", value=total_rents)

with col2:
    total_rents_casual = round(daily_rent_casual.casual_hourly.sum())
    st.metric("Total casual users", value=total_rents_casual)

with col3:
    total_rents_registered = round(daily_rent_registered.registered_hourly.sum())
    st.metric("Total registered users", value=total_rents_registered)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["date_time"],
    daily_rent_df["total_count_hourly"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
 
st.pyplot(fig)

#Performa Harian Berdasarkan Season
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x=weekday_rent_df["weekday_hourly"],
    y=weekday_rent_df["avg_count_weekday"],
    hue=weekday_rent_df['season_hourly'],
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Relation Season vs Daily Rents", loc='center', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

#Performa Harian Berdasarkan Weather Condition
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=weekday_rent_df["weekday_hourly"],
    y=weekday_rent_df["avg_count_weekday"],
    hue=weekday_rent_df['weather_condition_hourly'],
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Relation Weather Condition vs Daily Rents", loc='center', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# Performa Bulanan 
st.header('Monthly Rent')

st.subheader('Distibution Monthly by Season :')

col1, col2, col3, col4 = st.columns(4)

with col1: 
    springer_season=monthly_rent_df[monthly_rent_df['season_hourly']=='Springer']
    total_rents_springer = round(springer_season.sum_count_month.sum())
    st.metric("Total rent when Springer", value=total_rents_springer)

with col2:
    summer_season=monthly_rent_df[monthly_rent_df['season_hourly']=='Summer']
    total_rents_summer = round(summer_season.sum_count_month.sum())
    st.metric("Total rent when Summer", value=total_rents_summer)

with col3: 
    fall_season=monthly_rent_df[monthly_rent_df['season_hourly']=='Fall']
    total_rents_fall = round(fall_season.sum_count_month.sum())
    st.metric("Total rent when Fall", value=total_rents_fall)

with col4: 
    winter_season=monthly_rent_df[monthly_rent_df['season_hourly']=='Winter']
    total_rents_winter = round(winter_season.sum_count_month.sum())
    st.metric("Total rent when Winter", value=total_rents_winter)


fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(x="month_hourly", y="avg_count_month", data=monthly_rent_df, hue='season_hourly', ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Relation Season vs Monthly Rents", loc='center', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis ='x', labelsize=20)
st.pyplot(fig)

st.subheader('Distibution Monthly by Weather Condition :')

col1, col2 = st.columns(2)

with col1: 
    clear_weather=monthly_rent_df[monthly_rent_df['weather_condition_hourly']=='Clear, Few clouds, Partly cloudy, Partly cloudy']
    total_rents_clear = round(clear_weather.sum_count_month.sum())
    st.metric("Total rent when the Weather is Clear", value=total_rents_clear)

with col2:
    mist_weather=monthly_rent_df[monthly_rent_df['weather_condition_hourly']=='Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist']
    total_rents_mist = round(mist_weather.sum_count_month.sum())
    st.metric("Total rent when the Weather is Mist + Cloudly", value=total_rents_mist)

col1, col2 = st.columns(2)
with col1:
    snow_weather=monthly_rent_df[monthly_rent_df['weather_condition_hourly']=='Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds']
    total_rents_snow = round(snow_weather.sum_count_month.sum())
    st.metric("Total rent when the Weather is Light Snow + Rain", value=total_rents_snow)

with col2: 
    heavy_weather=monthly_rent_df[monthly_rent_df['weather_condition_hourly']=='Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog']
    total_rents_heavy = round(heavy_weather.sum_count_month.sum())
    st.metric("Total rent when the Weather is Dangerous", value=total_rents_heavy)

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='month_hourly', y='avg_count_month', data=monthly_rent_df, hue='weather_condition_hourly', ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis ='x', labelsize=20)

st.pyplot(fig)

st.subheader("Relation Holiday/Working Day vs Total Rents")
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='holiday_hourly', y='total_count_hourly', data=holiday_df, ax=ax)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.subheader("Clusters of bikeshare rides by season and temperature (2011-2012)")


fig, ax = plt.subplots(figsize=(16,8))

sns.scatterplot(x='temp_hourly', y='total_count_hourly', data=temp_df, hue='season_hourly', ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis ='x', labelsize=20)

st.pyplot(fig)

st.caption('Copyright © Paul John Binsar Ganda Silaban 2024')
