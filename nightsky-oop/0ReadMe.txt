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
