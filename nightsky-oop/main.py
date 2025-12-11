# main.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Entry point for NightSky Helper; menu logic and user interaction

# Import modules to support program execution
from models import Observation
from sky_calculator import SkyCalculator
from data_storage import load_observations, save_observations
from utils import get_user_date, display_results

def main_menu():
    # Main function runs user menu and program execution

    results: list[Observation] = load_observations()

    while True:
        print("\nWould you like to (1) check another date, (2) save to file, (3) view saved results, or (4) quit? ")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            obs_date = get_user_date()
            calculator = SkyCalculator()
            observation = calculator.calculate(obs_date)
            results.append(observation)
            display_results(observation)

        elif choice == '2':
            save_observations(results)

        elif choice == '3':
            saved_results = load_observations()
            if not saved_results:
                print("\nNo saved results found.")
            for obs in saved_results:
                display_results(obs)

        elif choice == '4':
            print("Goodbye, happy stargazing!")
            return

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    print("Welcome to NightSky Helper!")

    # Load previous results if any
    results = load_observations()
    if results:
        print(f"Loaded {len(results)} past observation(s) from 'nightsky_results.csv'.")

    # Run one observation
    obs_date = get_user_date()
    calculator = SkyCalculator()
    observation = calculator.calculate(obs_date)
    results.append(observation)
    display_results(observation)

    # Start main menu
    main_menu()