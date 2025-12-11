Modular Layout (8 files):

nightsky_helper/nightsky-oop/
|
|-- main.py                    Entry point (menu logic)
|-- sky_calculator.py          Sky calculation logic (Skyfield) ... SkyCalculator class
|-- data_storage.py            Load/save CSV
|-- celestial_objects.py       Planet/star definitions
|-- location.py                Location and timezone handling ... Location class
|-- models.py                  Data classes for Observation, Location ... Observation class
|-- moon.py                    Web scraping moon illumination data
|-- utils.py                   Helpers (formatting, datetime, etc.)

User Instructions 

Before running the program, install the following Python packages so they can be imported by the modules: skyfield, pytz, requests. (In your command prompt, type “pip install skyfield pytz requests”.) These packages provide astronomical calculations, time-zone handling, and web data functionality.

With all 8 module files in the same directory, run the application from a terminal or command prompt: python main.py

You will see a welcome message. If you have any previously saved results, the program will automatically load them from nightsky_results.csv and tell you how many were found. You will then be prompted to enter a date for your first observation.

Type your desired observation date in the format YYYY-MM-DD. The program computes astronomical data for that date and your results are immediately displayed and stored in memory. You can choose option 2 to save these results to the CSV file. 

You can choose option 1 from the main menu to enter another date for observation, or you can choose option 3 to view all of the saved results. 
Type option 4 to quit the program. All unsaved results remain in the program’s memory only, so these will be lost if you don't save them first.

Questions? Email me or send me a GitHub or LinkedIn message. Contact information is on my portfolio: https://cvcpatton.github.io/index.html 
