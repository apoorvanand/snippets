from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

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
    tags=['wind_simulation']
)
def wind_simulation_dag():

    @task
    def simulate_wind_speed(v_char: float, num_samples: int) -> list:
        """Simulate wind speeds using the given characteristic velocity."""
        result = v_char * np.sqrt(-np.log(1 - np.random.rand(num_samples)))
        return result.tolist()

    @task
    def simulate_monthly_max_wind_speed(v_char: float, days_per_month: int, num_simulations: int) -> list:
        """Simulate monthly maximum wind speeds."""
        max_speeds = []
        for _ in range(num_simulations):
            daily_speeds = v_char * np.sqrt(-np.log(1 - np.random.rand(days_per_month)))
            max_speeds.append(float(np.max(daily_speeds)))
        return max_speeds

    @task
    def generate_plot(rotterdam_wind: list, vienna_wind: list, 
                     rotterdam_max: list, vienna_max: list) -> str:
        """Generate and save the wind speed distribution plot."""
        plt.figure(figsize=(12, 6))
        
        plt.hist(rotterdam_wind, bins=30, alpha=0.5, label='Rotterdam regular wind')
        plt.hist(rotterdam_max, bins=30, alpha=0.5, label='Rotterdam monthly maxima')
        plt.hist(vienna_wind, bins=30, alpha=0.5, label='Vienna regular wind')
        plt.hist(vienna_max, bins=30, alpha=0.5, label='Vienna monthly maxima')
        
        plt.xlabel('Wind speed (m/s)')
        plt.ylabel('Frequency')
        plt.title('Monte Carlo Simulation of Wind Speeds')
        plt.legend()
        
        # Save the plot instead of displaying it
        plot_path = '/opt/airflow/dags/wind_simulation_plot.png'
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path

    @task
    def calculate_statistics(rotterdam_wind: list, vienna_wind: list, 
                           rotterdam_max: list, vienna_max: list) -> dict:
        """Calculate basic statistics for the simulated wind speeds."""
        return {
            'rotterdam_mean': np.mean(rotterdam_wind),
            'vienna_mean': np.mean(vienna_wind),
            'rotterdam_max_mean': np.mean(rotterdam_max),
            'vienna_max_mean': np.mean(vienna_max)
        }

    # Define parameters
    v_char_rotterdam = 10.67229219
    v_char_vienna = 8.542709123
    days_per_month = 30
    num_simulations = 1000

    # Execute tasks
    rotterdam_wind = simulate_wind_speed(v_char_rotterdam, num_simulations)
    vienna_wind = simulate_wind_speed(v_char_vienna, num_simulations)
    
    rotterdam_max = simulate_monthly_max_wind_speed(
        v_char_rotterdam, days_per_month, num_simulations
    )
    vienna_max = simulate_monthly_max_wind_speed(
        v_char_vienna, days_per_month, num_simulations
    )

    # Generate plot and calculate statistics
    plot_path = generate_plot(rotterdam_wind, vienna_wind, rotterdam_max, vienna_max)
    stats = calculate_statistics(rotterdam_wind, vienna_wind, rotterdam_max, vienna_max)

    # Set up dependencies (though TaskFlow handles this automatically)
    [rotterdam_wind, vienna_wind, rotterdam_max, vienna_max] >> plot_path >> stats

# Create the DAG
wind_simulation = wind_simulation_dag()
