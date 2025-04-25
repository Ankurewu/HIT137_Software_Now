import os
import re
import pandas as pd

# Directory containing temperature CSV files
DATA_DIR = 'temperature_data'
FILE_PATTERN = r"stations_group_\d{4}\.csv"

# Define seasons and corresponding months
SEASONS = {
    'Spring': ['September', 'October', 'November'],
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August']
}

def get_csv_files(directory, pattern):
    return [file for file in os.listdir(directory) if re.match(pattern, file)]

def read_and_combine_csvs(file_list, directory):
    return pd.concat(
        [pd.read_csv(os.path.join(directory, file)) for file in file_list],
        ignore_index=True
    )

def compute_seasonal_averages(df, seasons):
    for season, months in seasons.items():
        df[season] = df[months].mean(axis=1)
    return df

def save_seasonal_averages(df, seasons, output_file='average_temp.txt'):
    with open(output_file, 'w') as f:
        for season in seasons:
            avg_temp = df[season].mean()
            f.write(f"{season} Average Temperature: {avg_temp:.2f}°C\n")

def identify_extreme_stations(df, temp_columns):
    df['Temp_Range'] = df[temp_columns].max(axis=1) - df[temp_columns].min(axis=1)
    df['Max_Temperature'] = df[temp_columns].max(axis=1)
    df['Min_Temperature'] = df[temp_columns].min(axis=1)

    largest_range = df.loc[df['Temp_Range'] == df['Temp_Range'].max()]
    warmest = df.loc[df['Max_Temperature'] == df['Max_Temperature'].max()]
    coolest = df.loc[df['Min_Temperature'] == df['Min_Temperature'].min()]

    return largest_range, warmest, coolest

def save_extremes_to_file(largest_range, warmest, coolest):
    with open('largest_temp_range_station.txt', 'w') as f:
        f.write("Station(s) with largest temperature range:\n")
        for _, row in largest_range.iterrows():
            f.write(f"{row['STATION_NAME']} (Temperature Range: {row['Temp_Range']:.2f}°C)\n")

    with open('warmest_and_coolest_station.txt', 'w') as f:
        f.write("Warmest Station(s):\n")
        for _, row in warmest.iterrows():
            f.write(f"{row['STATION_NAME']} (Max Temperature: {row['Max_Temperature']:.2f}°C)\n")

        f.write("\nCoolest Station(s):\n")
        for _, row in coolest.iterrows():
            f.write(f"{row['STATION_NAME']} (Min Temperature: {row['Min_Temperature']:.2f}°C)\n")

def main():
    try:
        csv_files = get_csv_files(DATA_DIR, FILE_PATTERN)
        if not csv_files:
            print("No matching CSV files found.")
            return

        df_combined = read_and_combine_csvs(csv_files, DATA_DIR)

        # Columns assumed to be month names, usually start from 4th column onward
        temp_columns = df_combined.columns[4:16]

        df_with_seasons = compute_seasonal_averages(df_combined, SEASONS)
        save_seasonal_averages(df_with_seasons, SEASONS)

        largest_range, warmest, coolest = identify_extreme_stations(df_with_seasons, temp_columns)
        save_extremes_to_file(largest_range, warmest, coolest)

        print("Temperature analysis complete. Output files saved.")
    
    except FileNotFoundError:
        print("Directory or file not found.")
    except pd.errors.EmptyDataError:
        print("One of the CSV files is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
