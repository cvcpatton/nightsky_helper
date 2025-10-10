# nightsky-basic.py - Cathy Patton, 10/9/25, Basic console version

"""
Python program using Skyfield (library) to calculate stargazing times
and visible celestial objects with CSV export for the Denver area.
Location coordinates and timezone may be updated for other areas.
"""

# Import modules to support program execution
import csv
from datetime import datetime, timedelta
from skyfield.api import load, Star, Topos
from skyfield.almanac import find_discrete, dark_twilight_day
import pytz

# Constants for location (Denver coordinates)
LATITUDE = 39.7392
LONGITUDE = -104.9903
DENVER_TZ = pytz.timezone('America/Denver')

# Dictionaries for selected celestial objects for use in calculations/display
CELESTIAL_OBJECTS = {
    'planets': ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
    'stars': ['Sirius', 'Arcturus', 'Vega', 'Capella', 'Rigel', 'Procyon', 'Betelgeuse']
}

# Planet names to match Skyfield ephemeris data (outer planets use barycenter for accuracy)
PLANET_MAP = {
    'Mercury': 'mercury',
    'Venus': 'venus',
    'Mars': 'mars',
    'Jupiter': 'jupiter barycenter',
    'Saturn': 'saturn barycenter',
    'Uranus': 'uranus barycenter',
    'Neptune': 'neptune barycenter'
}

# Mapping common Star names to Skyfield's Star() object celestial coordinates (RA/Dec)
STAR_COORDS = {
    'Sirius': Star(ra_hours=6 + 45/60 + 8.9/3600, dec_degrees=-16 - 42/60 - 58/3600),
    'Arcturus': Star(ra_hours=14 + 15/60 + 39.7/3600, dec_degrees=19 + 10/60 + 56/3600),
    'Vega': Star(ra_hours=18 + 36/60 + 56.3/3600, dec_degrees=38 + 47/60 + 1/3600),
    'Capella': Star(ra_hours=5 + 16/60 + 41.4/3600, dec_degrees=45 + 59/60 + 52/3600),
    'Rigel': Star(ra_hours=5 + 14/60 + 32.3/3600, dec_degrees=-8 - 12/60 - 6/3600),
    'Procyon': Star(ra_hours=7 + 39/60 + 18.1/3600, dec_degrees=5 + 13/60 + 30/3600),
    'Betelgeuse': Star(ra_hours=5 + 55/60 + 10.3/3600, dec_degrees=7 + 24/60 + 25/3600)
}

# Global list to store multiple stargazing results
results = []

def to_utc(local_dt):
    # Convert localized datetime to UTC
    return DENVER_TZ.localize(local_dt).astimezone(pytz.utc)

def format_time(dt):
    # Formatted time for clean output (12-hour format with AM/PM and no leading zeroes)
    return dt.strftime("%I:%M %p").lstrip("0") if dt else "Unavailable"

def get_user_date():
    # Prompt user for valid stargazing date, format YYYY-MM-DD, ensure date is today or in the future
    while True:
        try:
            date_input = input("Enter a date for stargazing (YYYY-MM-DD): ")
            user_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            if user_date < datetime.today().date():
                print("That date is in the past. Please enter today's date or a future date.")
            else:
                return user_date
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")
            exit()

def calculate_sky_data(obs_date):
    # Use Skyfield library to calculate visible planets and stars

    # Load ephemeris data from Skyfield (de421.bsp includes planets and the moon)
    eph = load('de421.bsp')
    ts = load.timescale() # Load Skyfield's timescale system
    # Define observer's geographic location (Denver, CO)
    observer = Topos(latitude_degrees=LATITUDE, longitude_degrees=LONGITUDE)
    location = eph['earth'] + observer # Combine Earth with observer's position

    # Set up two time points for event search: noon of the observation day and 2 days later
    local_noon = datetime(obs_date.year, obs_date.month, obs_date.day, 12)
    t0 = ts.utc(to_utc(local_noon)) # Convert to UTC Skyfield time
    t1 = ts.utc(to_utc(local_noon + timedelta(days=2))) # Range ends 2 days later

    # Use Skyfield's dark_twilight_day() function to find sunset, darkness, and sunrise events
    f = dark_twilight_day(eph, observer) # Returns an event function for light/dark transitions
    times, events = find_discrete(t0, t1, f) # Find all events (sunset, sunrise, etc.) in the time range

    # Create a list of (event_type, local_time) tuples for easier filtering
    event_log = [(e, DENVER_TZ.normalize(t.utc_datetime().replace(tzinfo=pytz.utc).astimezone(DENVER_TZ)))
                 for t, e in zip(times, events)]

    # Identify sunset time on the observation date (event 1 = sunset)
    sunset = next((lt for e, lt in reversed(event_log) if e == 1 and lt.date() == obs_date), None)
    # Identify the time when the sky becomes fully dark (event 0 = end of twilight)
    dark_start = next((lt for e, lt in event_log if e == 0 and sunset and lt > sunset and lt.date() == obs_date), None)
    # Identify sunrise on the following day (event 3 = sunrise)
    sunrise = next((lt for e, lt in event_log if e == 3 and lt.date() == obs_date + timedelta(days=1)), None)

    # Define the time for checking visibility: 10:00 PM local time on the observation date
    t_night = ts.utc(to_utc(datetime(obs_date.year, obs_date.month, obs_date.day, 22)))

    # Determine which planets are visible above the horizon at 10 PM
    visible_planets = [
        name for name in CELESTIAL_OBJECTS['planets']
        if (eph_name := PLANET_MAP.get(name)) and eph_name in eph
        and location.at(t_night).observe(eph[eph_name]).apparent().altaz()[0].degrees > 0
    ]

    # Determine which stars are visible above the horizon at 10 PM
    visible_stars = [
        name for name in CELESTIAL_OBJECTS['stars']
        if (star := STAR_COORDS.get(name)) and
        location.at(t_night).observe(star).apparent().altaz()[0].degrees > 0
    ]

    """
    Note: The dates I was testing (2025, 10-05, 10-25, 11-01, 11-10) seemed to give incorrect results. 
    However, DST begins at 3AM on 11-02, and that allows for what looks like a miscalculation.
    """

    # Return all relevant stargazing data in a dictionary
    return {
        'date': obs_date.isoformat(),
        'sunset': format_time(sunset),
        'dark_sky': format_time(dark_start),
        'sunrise': format_time(sunrise),
        'planets': visible_planets,
        'stars': visible_stars
    }

def display_results(observation):
    # Display the results to the user
    print(f"\nStargazing Info for {observation['date']}:")
    print(f"  Sunset: {observation['sunset']}")
    print(f"  Dark Sky Begins: {observation['dark_sky']}")
    print(f"  Sunrise: {observation['sunrise']}")
    print("  Visible Planets:", ', '.join(observation['planets']))
    print("  Prominent Stars:", ', '.join(observation['stars']))

def save_to_csv(data_list, filename="nightsky_results.csv"):
    # Save observations to CSV
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Sunset', 'Dark sky', 'Sunrise', 'Planets', 'Stars'])
            for data in data_list:
                writer.writerow([
                    data['date'], data['sunset'], data['dark_sky'], data['sunrise'],
                    ';'.join(data['planets']), ';'.join(data['stars'])
                ])
        print(f"{len(data_list)} observation(s) saved to '{filename}'.")
    except PermissionError:
        print(f"Permission denied: '{filename}'. Check permissions.")
    except OSError as e:
        print(f"Error saving to file: {e}")

def load_from_csv(filename="nightsky_results.csv"):
    # Load saved observations from CSV
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [{
                'date': row['Date'],
                'sunset': row['Sunset'],
                'dark_sky': row['Dark sky'],
                'sunrise': row['Sunrise'],
                'planets': row['Planets'].split(';') if row['Planets'] else [],
                'stars': row['Stars'].split(';') if row['Stars'] else []
            } for row in reader]
    except FileNotFoundError:
        print(f"No saved data found in '{filename}'. Starting fresh.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def print_saved_results(filename="nightsky_results.csv"):
    # Reads and displays saved results from CSV
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            if not rows:
                print("\nNo saved results to display.")
                return

            print("\nSaved Stargazing Observations:")
            for row in rows:
                print(f"\nDate: {row['Date']}")
                print(f"  Sunset: {row['Sunset']}")
                print(f"  Dark Sky Begins: {row['Dark sky']}")
                print(f"  Sunrise: {row['Sunrise']}")
                planets = row['Planets'].replace(';', ', ')
                stars = row['Stars'].replace(';', ', ')
                print(f"  Visible Planets: {planets if planets else 'None'}")
                print(f"  Prominent Stars: {stars if stars else 'None'}")
    except FileNotFoundError:
        print(f"\nNo file named '{filename}' found.")
    except Exception as e:
        print(f"\nError reading saved results: {e}")

def main_menu():
    # Main function runs user menu and program execution

    global results
    results = load_from_csv()

    while True:
        print("\nWould you like to (1) check another date, (2) save to file, (3) view saved results, or (4) quit? ")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            obs_date = get_user_date()
            observation = calculate_sky_data(obs_date)
            results.append(observation)
            display_results(observation)

        elif choice == '2':
            save_to_csv(results)

        elif choice == '3':
            print_saved_results()

        elif choice == '4':
            print("Goodbye, happy stargazing!")
            return

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    print("Welcome to NightSky Helper!")
    results = load_from_csv()
    if results:
        print(f"Loaded {len(results)} past observation(s) from 'nightsky_results.csv'.")
    obs_date = get_user_date()
    observation = calculate_sky_data(obs_date)
    results.append(observation)
    display_results(observation)

    main_menu()
