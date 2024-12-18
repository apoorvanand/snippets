from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['weather_simulation']
)
def weather_simulation_dag():
    
    @task
    def generate_weather_data():
        np.random.seed(42)
        num_days = 365
        num_params = 3
        
        weather_data = np.random.rand(num_days, num_params) * [30, 100, 50]
        
        # Normalize the data
        weather_data[:, 0] = weather_data[:, 0] * 20 + 10
        weather_data[:, 1] = weather_data[:, 1] * 80 + 20
        weather_data[:, 2] = weather_data[:, 2] * 40 + 10
        
        return weather_data.tolist()  # Convert numpy array to list for XCom

    @task
    def create_dataframe(weather_data):
        df = pd.DataFrame(
            weather_data, 
            columns=['Temperature (C)', 'Humidity (%)', 'Wind Speed (km/h)']
        )
        return df.to_dict()  # Convert DataFrame to dictionary for XCom

    @task
    def plot_weather_data(df_dict):
        df = pd.DataFrame.from_dict(df_dict)
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 3, 1)
        plt.plot(df['Temperature (C)'])
        plt.title('Temperature')

        plt.subplot(1, 3, 2)
        plt.plot(df['Humidity (%)'])
        plt.title('Humidity')

        plt.subplot(1, 3, 3)
        plt.plot(df['Wind Speed (km/h)'])
        plt.title('Wind Speed')
        
        plt.tight_layout()
        
        # Save plot instead of showing it
        plt.savefig('/opt/airflow/dags/weather_plot.png')
        plt.close()
        
        return "Plot saved successfully"

    @task
    def print_data_summary(df_dict):
        df = pd.DataFrame.from_dict(df_dict)
        summary = df.head().to_string()
        print("First few rows of the weather data:")
        print(summary)
        return summary

    # Define the task dependencies
    weather_data = generate_weather_data()
    df_dict = create_dataframe(weather_data)
    plot = plot_weather_data(df_dict)
    summary = print_data_summary(df_dict)
    
    # Set dependencies
    weather_data >> df_dict >> [plot, summary]

# Create the DAG
weather_dag = weather_simulation_dag()
