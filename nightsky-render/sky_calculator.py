# sky_calculator.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Handles astronomical calculations using Skyfield

from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, dark_twilight_day
from datetime import datetime, timedelta
import pytz
from models import Observation
from celestial_objects import CELESTIAL_OBJECTS, PLANET_MAP, STAR_COORDS
from location import DENVER, format_time
from moon import get_moon_illumination

class SkyCalculator:
    def __init__(self):
        self.eph = load('de421.bsp')
        self.ts = load.timescale()
        self.observer = DENVER
        self.tz = DENVER.tz

    def calculate(self, obs_date: datetime.date) -> Observation:
        observer_loc = self.eph['earth'] + self.observer.topos

        # Noon of observation date, correctly localized with DST awareness
        local_noon = datetime(obs_date.year, obs_date.month, obs_date.day, 12)
        local_noon = self.tz.localize(local_noon, is_dst=None)

        t0 = self.ts.utc(local_noon.astimezone(pytz.utc))
        t1 = self.ts.utc((local_noon + timedelta(days=2)).astimezone(pytz.utc))

        f = dark_twilight_day(self.eph, self.observer.topos)
        times, events = find_discrete(t0, t1, f)

        # Convert each Skyfield UTC time to local Denver time
        event_log = [
            (e, t.utc_datetime().replace(tzinfo=pytz.utc).astimezone(self.tz))
            for t, e in zip(times, events)
        ]

        # Identify sunset, dark_sky, and sunrise
        sunset = next((lt for e, lt in reversed(event_log) if e == 1 and lt.date() == obs_date), None)
        dark_start = next((lt for e, lt in event_log if e == 0 and sunset and lt > sunset and lt.date() == obs_date), None)
        sunrise = next((lt for e, lt in event_log if e == 3 and lt.date() == obs_date + timedelta(days=1)), None)

        # 10 PM local time for visible objects
        local_night = datetime(obs_date.year, obs_date.month, obs_date.day, 22)
        local_night = self.tz.localize(local_night, is_dst=None)
        t_night = self.ts.utc(local_night.astimezone(pytz.utc))

        # Visible planets
        visible_planets = [
            name for name in CELESTIAL_OBJECTS['planets']
            if (eph_name := PLANET_MAP.get(name)) and eph_name in self.eph
            and observer_loc.at(t_night).observe(self.eph[eph_name]).apparent().altaz()[0].degrees > 0
        ]

        # Visible stars
        visible_stars = [
            name for name in CELESTIAL_OBJECTS['stars']
            if (star := STAR_COORDS.get(name)) and
            observer_loc.at(t_night).observe(star).apparent().altaz()[0].degrees > 0
        ]

        moon_illum = get_moon_illumination(obs_date)

        return Observation(
            date=obs_date.isoformat(),
            sunset=format_time(sunset),
            dark_sky=format_time(dark_start),
            sunrise=format_time(sunrise),
            planets=visible_planets,
            stars=visible_stars,
            moon_illum=moon_illum
        )

