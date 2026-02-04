# data_storage.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# CSV load/save/display logic

# Import modules to support program execution
import csv
from models import Observation

FILENAME = "nightsky_results.csv"

def save_observations(obs_list: list[Observation], filename=FILENAME):
    # Save observations to CSV including moon impact
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Add Moon Impact column
        writer.writerow([
            'Date', 'Sunset', 'Dark sky', 'Sunrise', 'Planets', 'Stars', 'Moon Illumination', 'Moon Impact'
        ])
        for obs in obs_list:
            # Calculate moon impact dynamically
            try:
                moon_pct = int(obs.moon_illum.strip('%'))
                if moon_pct >= 50:
                    moon_impact = "The moon's brightness could interfere with stargazing activity."
                elif 25 <= moon_pct < 50:
                    moon_impact = "The moon may slightly affect stargazing visibility."
                else:
                    moon_impact = "Moonlight should have minimal impact on stargazing."
            except (ValueError, AttributeError):
                moon_impact = "N/A"

            writer.writerow([
                obs.date,
                obs.sunset,
                obs.dark_sky,
                obs.sunrise,
                ';'.join(obs.planets),
                ';'.join(obs.stars),
                obs.moon_illum,
                moon_impact
            ])
    print(f"{len(obs_list)} observation(s) saved to '{filename}'.")

def load_observations(filename=FILENAME) -> list[Observation]:
    # Load saved observations from CSV
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [
                Observation(
                    date=row['Date'],
                    sunset=row['Sunset'],
                    dark_sky=row['Dark sky'],
                    sunrise=row['Sunrise'],
                    planets=row['Planets'].split(';') if row['Planets'] else [],
                    stars=row['Stars'].split(';') if row['Stars'] else [],
                    moon_illum=row.get('Moon Illumination', 'N/A')
                )
                for row in reader
            ]
    except FileNotFoundError:
        return []