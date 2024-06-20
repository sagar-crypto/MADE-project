import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def load_data(database_path):
    engine = create_engine(f'sqlite:///{database_path}')
    crop_irrigated = pd.read_sql_table('crop_irrigated', con=engine)
    crop_not_irrigated = pd.read_sql_table('crop_not_irrigated', con=engine)
    climate_change = pd.read_sql_table('climate_change', con=engine)

    max_irrigated_value = crop_irrigated['Value'].max().replace(',', '')
    max_not_irrigated_value = crop_not_irrigated['Value'].max().replace(',', '')
    min_irrigated_value = crop_irrigated['Value'].min().replace(',', '')
    min_not_irrigated_value = crop_not_irrigated['Value'].min().replace(',', '')
    return crop_irrigated, crop_not_irrigated, climate_change, max_irrigated_value, max_not_irrigated_value, min_irrigated_value, min_not_irrigated_value

def plot_data(crop_irrigated, crop_not_irrigated, climate_change, output_directory, max_irrigated_value, max_not_irrigated_value, min_irrigated_value, min_not_irrigated_value):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    min_y_value = int(min(min_irrigated_value,min_not_irrigated_value))
    max_y_value = int(max(max_irrigated_value,max_not_irrigated_value))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=crop_irrigated, x='Year', y='Value', label='Irrigated')
    sns.lineplot(data=crop_not_irrigated, x='Year', y='Value', label='Not Irrigated')
    plt.title('Corn Yield Over Time')
    plt.xlabel('Year')
    plt.ylabel('Yield (bushels per acre)')
    plt.legend()
    plt.yticks(range(min_y_value, max_y_value + 1, 50000))
    plt.savefig(os.path.join(output_directory, 'corn_yield_over_time.png'))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=climate_change, x='Year', y='Temperature')
    plt.title('Temperature Over Time')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.savefig(os.path.join(output_directory, 'temperature_over_time.png'))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=climate_change, x='Year', y='CO2 Emissions')
    plt.title('CO2 Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (ppm)')
    plt.savefig(os.path.join(output_directory, 'co2_emissions_over_time.png'))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=climate_change, x='Year', y='Sea Level Rise')
    plt.title('Sea Level Rise Over Time')
    plt.xlabel('Year')
    plt.ylabel('Sea Level Rise (mm)')
    plt.savefig(os.path.join(output_directory, 'sea_level_rise_over_time.png'))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=climate_change, x='Year', y='Precipitation')
    plt.title('Precipitation Over Time')
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')
    plt.savefig(os.path.join(output_directory, 'precipitation_over_time.png'))

    plt.figure(figsize=(16, 10))
    sns.lineplot(data=climate_change, x='Year', y='Temperature', color='red', label='Temperature', marker='o')
    for year, temperature in zip(climate_change['Year'], climate_change['Temperature']):
        plt.text(year, temperature, f"{temperature:.1f}°C", fontsize=8, ha='center', va='bottom')

    sns.lineplot(data=crop_irrigated, x='Year', y='Value', label='Irrigated', color='green')
    sns.lineplot(data=crop_not_irrigated, x='Year', y='Value', label='Not Irrigated', color='blue')

    plt.title('Yield vs Temperature')
    plt.xlabel('Year')
    plt.ylabel('Yield (bushels per acre) / Temperature (°C)')
    plt.legend()
    plt.yticks(range(min_y_value, max_y_value + 1, 50000))

    plt.savefig(os.path.join(output_directory, 'yield_vs_temperature.png'))

def main():
    database_path = '../data/Data.sqlite'
    output_directory = '../plots/'

    crop_irrigated, crop_not_irrigated, climate_change, max_irrigated_value, max_not_irrigated_value,min_irrigated_value, min_not_irrigated_value = load_data(database_path)
    plot_data(crop_irrigated, crop_not_irrigated, climate_change, output_directory, max_irrigated_value, max_not_irrigated_value, min_irrigated_value, min_not_irrigated_value)

if __name__ == "__main__":
    main()
