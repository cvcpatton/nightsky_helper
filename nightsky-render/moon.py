# moon.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Advanced feature - web scraping Moon Illumination data for user input date from a CSV source

# Import modules to support program execution
import requests
from datetime import datetime

def get_moon_illumination(user_date: datetime.date) -> str:
    """
    Scrapes the moon illumination percentage for the given date from a CSV file.
    Returns a string like '45%' or 'N/A' if not found.
    """
    url = "https://raw.githubusercontent.com/isaacbernat/moon-data/main/moon_phases_UTC_1800-2050.csv"

    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.RequestException:
        return "N/A"

    content = resp.text.strip().splitlines()

    # The CSV format is: date,illumination_fraction
    for line in content[1:]:  # skip header
        parts = line.split(",")
        if len(parts) < 2:
            continue
        date_str, illum_frac = parts[0], parts[1]
        try:
            row_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if row_date == user_date:
                # Convert fraction to percentage
                percentage = round(float(illum_frac) * 100)
                return f"{percentage}%"
        except ValueError:
            continue

    return "N/A"