# models.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Data class for Observation

# Import modules to support program execution
from dataclasses import dataclass
from typing import List

@dataclass
class Observation:
    date: str
    sunset: str
    dark_sky: str
    sunrise: str
    planets: List[str]
    stars: List[str]
    moon_illum: str = "N/A" # default value