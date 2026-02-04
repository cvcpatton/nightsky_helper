# celestial_objects.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Contains celestial object data and helper functions for NightSky Helper

# Import modules to support program execution
from skyfield.api import Star

# Selected celestial objects for calculations/display
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