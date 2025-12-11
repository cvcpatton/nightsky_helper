# utils.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# General utility functions

# Import modules to support program execution
from datetime import datetime
from models import Observation

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

def display_results(observation: Observation):
    # Display the results to the user
    print(f"\nStargazing Info for {observation.date}:")
    print(f"  Sunset: {observation.sunset}")
    print(f"  Dark Sky Begins: {observation.dark_sky}")
    print(f"  Sunrise: {observation.sunrise}")
    print("  Visible Planets:", ', '.join(observation.planets) if observation.planets else "None")
    print("  Prominent Stars:", ', '.join(observation.stars) if observation.stars else "None")
    print(f"  Moon Illumination: {observation.moon_illum}")

    # Moon impact warning for output
    try:
        moon_pct = int(observation.moon_illum.strip('%'))
        if moon_pct >= 50:
            warning = "The moon's brightness could interfere with stargazing activity."
        elif 25 <= moon_pct < 50:
            warning = "The moon may slightly affect stargazing visibility."
        else:
            warning = "Moonlight should have minimal impact on stargazing."
        print(f"  Moon Impact: {warning}")
    except ValueError:
        print("  Moon Impact: N/A")