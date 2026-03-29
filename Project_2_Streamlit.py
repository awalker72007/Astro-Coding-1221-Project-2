import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, wgs84
from skyfield import almanac
from datetime import datetime, timedelta
import astropy
from skyfield.framelib import ecliptic_frame
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, get_body
from astropy.time import Time
import datetime
import astropy.units as u
from astroquery.simbad import Simbad
from astroplan import Observer, FixedTarget
from astropy.visualization import astropy_mpl_style, quantity_support
import streamlit as st
import os

eph = load('de440s.bsp')
ephemeris = eph 
#Using the de440s emphemeris file for the locations

bodies = {
    "sun": eph['sun'],
    "moon": eph['moon'],
    "pluto": eph['pluto barycenter'],
    "mars": eph['mars barycenter'],
    "jupiter": eph['jupiter barycenter'],
    "saturn": eph['saturn barycenter'],
    "uranus": eph['uranus barycenter'],
    "venus": eph['venus barycenter'],
    "mercury": eph['mercury barycenter'],
}
#Grabbing the planets from the emphemeris and naming them
sun = eph['sun']
earth = eph['earth']

ts = load.timescale()
#Skyfield's time system
days = np.arange(0, 90)
global t_variable
t_variable = ts.utc(2026, 3, 1 + days)
t_start = ts.utc(2026, 3, 1)
t_end = ts.utc(2026, 3, 1 + 90)


now = Time.now()
days =np.linspace(0, 90, 24*91)
times = now + days * u.day
#making time array thing

#altaz_frames = AltAz(obstime=times, location=columbus)
#getting altaz from times


columbus_lat = 39.9612
columbus_lon = -83.0003
columbus_elev = 260
#Location of Columbus, Ohio (observation point for our code)

columbus = earth + wgs84.latlon(columbus_lat, columbus_lon, elevation_m = columbus_elev)
#Creating the observer to call from


def is_planet_in_sky(self, t0, t1):
    #t0 is the start time, t1 is the end time of observation
    t, y = almanac.find_risings(columbus, self, t0, t1)



def moon_phase():

    
    percent_illuminated = 100 * columbus.at(t_variable).observe(eph['moon']).fraction_illuminated(eph['sun'])
    
    _, sunlong, _ = columbus.at(t_variable).observe(eph['sun']).apparent().frame_latlon(ecliptic_frame)
    _, moonlong, _ = columbus.at(t_variable).observe(eph['moon']).apparent().frame_latlon(ecliptic_frame)
    phase = (np.asarray(moonlong.degrees) - np.asarray(sunlong.degrees)) % 360
    illumination = np.asarray(percent_illuminated)

    conditions = [
        (phase >= 2) & (phase <= 88),
        (phase > 88) & (phase < 92),
        (phase >= 92) & (phase <= 178),
        (phase > 178) & (phase < 182),
        (phase >= 182) & (phase <= 268),
        (phase > 268) & (phase < 272),
        (phase >= 272) & (phase <= 358),
    ]
    labels = [
        'Waxing Crescent',
        'First Quarter',
        'Waxing Gibbous',
        'Full Moon',
        'Waning Gibbous',
        'Last Quarter',
        'Waning Crescent',
    ]
    phase_name = np.select(conditions, labels, default='New Moon')

    moon_df = pd.DataFrame({
        'percent_illuminated': illumination,
        'phase_angle_deg': phase,
        'moon_phase': phase_name,
    })
    return moon_df

moon_phases_df = moon_phase()




def observation_from_user(body, planet_name):

    astrometric = columbus.at(t_variable).observe(body)
    apparent = astrometric.apparent()
    alt, az, distance = apparent.altaz(pressure_mbar=1010)
    t, y = almanac.find_risings(columbus, body, t_start, t_end)
    t, y = almanac.find_settings(columbus, body, t_start, t_end)
    n = len(alt.degrees)
    df = pd.DataFrame({
        'Planet': [planet_name] * n,
        'Altitude': alt.degrees,
        'Azimuth': az.degrees,
    })
    return(df)


for planet_name, body in bodies.items():
    df = observation_from_user(body, planet_name)
    print(planet_name)
    print(df)

#Singular day calculations
single_day = Time.now()
global single_day

def is_night():
    night_check = almanac.dark_twilight_day(eph, columbus_topos)
    night_state = night_check(single_day)
    return night_state <= 1

planet_cmaps = {
    "sun": "Accent",
    "moon": "Purples",
    "mercury": "Reds",
    "venus": "Oranges",
    "mars": "Greens",
    "jupiter": "Blues",
    "saturn": "Wistia",
    "uranus": "winter",
    "pluto": "spring",
}
cmap = plt.get_cmap(planet_cmaps.get(planet_name, "viridis"))

# Daily polar sky paths — run after the setup cell (needs `columbus`, `bodies`, `ts`).
N_SAMPLES_PER_DAY = 96  # samples from 0–24h UTC
def plot_all_planets_sky_path(year, month, day, n_samples=N_SAMPLES_PER_DAY):
    hours = np.linspace(0, 24, n_samples, endpoint=False)
    t_day = ts.utc(year, month, day, hours, 0)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(122, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 90)
    ax.set_yticks(range(0, 91, 30))
    ax.set_yticklabels(['90°', '60°', '30°', '0° (Horizon)'])

    tab = plt.cm.tab10(np.linspace(0, 1, max(10, len(bodies))))
    dfs = []
    for idx, (planet_name, body) in enumerate(bodies.items()):
        astrometric = columbus.at(t_day).observe(body)
        alt, az, _ = astrometric.apparent().altaz(pressure_mbar=1010)
        altd = np.asarray(alt.degrees)
        azdeg = np.asarray(az.degrees)
        n = len(altd)
        dfs.append(
            pd.DataFrame(
                {
                    'Planet': [planet_name] * n,
                    'Altitude': altd,
                    'Azimuth': azdeg,
                }
            )
        )
        mask = altd > 0
        if np.any(mask):
            c = tab[idx % len(tab)]
            mask_idx = np.where(mask)[0]
            # Split where visibility is not contiguous, so we do not draw
            # straight jump lines across below-horizon gaps.
            breaks = np.where(np.diff(mask_idx) > 1)[0] + 1
            chunks = np.split(mask_idx, breaks)

            first_chunk = True
            for chunk in chunks:
            # Define coordinates for this contiguous visible "chunk"
                theta_chunk = az.radians[chunk]
                r_chunk = 90 - altd[chunk]
            
            # Get the specific cmap for this planet inside the loop
                current_cmap = plt.get_cmap(planet_cmaps.get(planet_name, "viridis"))

            # Handle Azimuth wrapping (0 <-> 360) to prevent cross-chart streaks
                wrap_breaks = np.where(np.abs(np.diff(theta_chunk)) > np.pi)[0] + 1
                theta_sub_chunks = np.split(theta_chunk, wrap_breaks)
                r_sub_chunks = np.split(r_chunk, wrap_breaks)

            for th, rr in zip(theta_sub_chunks, r_sub_chunks):
                if len(th) < 2: 
                    # Plot a single point if it's too short for a line
                    ax.plot(th, rr, color=current_cmap(0.5), marker='o', markersize=3)
                    continue
                
                # Draw segments with gradient colors
                nseg = len(th) - 1
                for i in range(nseg):
                    seg_color = current_cmap(i / max(nseg, 1))
                    ax.plot(th[i:i+2], rr[i:i+2], color=seg_color, linewidth=2,
                            label=planet_name if (first_chunk and i == 0) else None)
            first_chunk = False

            
    ax.legend(loc='upper left', bbox_to_anchor=(1.08, 1.02), fontsize=9)
    ax.set_title(f'All bodies sky paths — {year}-{month:02d}-{day:02d} UTC', pad=12)
    plt.tight_layout()
    plt.show()
    return pd.concat(dfs, ignore_index=True)
    
    # Add every UTC day you want; each gets one figure and one entry in the dict.
DAYS_UTC = [
    (2026, 3, 1),
]
sky_path_df_by_day = {}
for y, m, d in DAYS_UTC:
    day_key = f"{y}-{m:02d}-{d:02d}"
    df_day = plot_all_planets_sky_path(y, m, d)
    sky_path_df_by_day[day_key] = df_day.assign(UTC_date=day_key)
for day_key, df_day in sky_path_df_by_day.items():
    print(f"{day_key}: {len(df_day)} rows")

N_SAMPLES_PER_DAY = 96  # samples from 0–24h UTC
def plot_all_planets_altitude_vs_time(year, month, day, n_samples=N_SAMPLES_PER_DAY):
    hours = np.linspace(0, 24, n_samples, endpoint=False)
    # Skyfield time array for each UTC hour
    # If this ever complains about float hours, use the t0 + seconds approach below instead.
    t_day = ts.utc(year, month, day, hours, 0)
    # t0 = ts.utc(year, month, day, 0, 0, 0)
    # t_day = t0 + hours * 3600
    fig, ax = plt.subplots()
    tab = plt.cm.tab10(np.linspace(0, 1, max(10, len(bodies))))
    dfs = []
    for idx, (planet_name, body) in enumerate(bodies.items()):
        astrometric = columbus.at(t_day).observe(body)
        alt, az, _ = astrometric.apparent().altaz(pressure_mbar=1010)
        altd = np.asarray(alt.degrees)
        azdeg = np.asarray(az.degrees)
        color = tab[idx % len(tab)]
        # Plot the full diurnal arc (negative altitude = below the horizon).
        ax.plot(hours, altd, color=color, linewidth=2, label=planet_name)
        n = len(altd)
        dfs.append(
            pd.DataFrame(
                {
                    "Planet": [planet_name] * n,
                    "UTC_hour": hours,
                    "Altitude": altd,
                    "Azimuth": azdeg,
                }
            )
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlim(0, 24)
    ax.set_ylim(-180, 180)
    ax.set_xlabel("UTC Hour")
    ax.set_ylabel("Altitude (degrees)")
    ax.set_title(f"All bodies altitude vs time — {year}-{month:02d}-{day:02d} UTC")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=5)
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_xticklabels([0, 6, 12, 18, 24])
    ax.set_yticks(range(-180, 181, 90))
    ax.set_yticklabels([-180, -90, '0 (Horizon)', 90, 180])
    
    plt.tight_layout()
    plt.show()
    return pd.concat(dfs, ignore_index=True)
DAYS_UTC = [
    (2026, 3, 1),
]
sky_path_df_by_day = {}
for y, m, d in DAYS_UTC:
    day_key = f"{y}-{m:02d}-{d:02d}"
    df_day = plot_all_planets_altitude_vs_time(y, m, d)
    sky_path_df_by_day[day_key] = df_day.assign(UTC_date=day_key)
for day_key, df_day in sky_path_df_by_day.items():
    print(f"{day_key}: {len(df_day)} rows")


st.title("Solar System Dashboard")
st.write("This Solar System Dashboard will track and display the positions of the planets (and the moon) in the sky in relation to Columbus, Ohio")
st.write("Select a date to see the positions of the planets in the sky")
DAYS_UTC = st.date_input("Select a date", )
if st.button("Plot Planets"):
    with st.spinner("Plotting planets..."):
        plot_all_planets_sky_path(DAYS_UTC.year, DAYS_UTC.month, DAYS_UTC.day)
        plot_all_planets_altitude_vs_time(DAYS_UTC.year, DAYS_UTC.month, DAYS_UTC.day)
        st.success("Planets plotted successfully!")
    st.image("image.png")
    st.image("image2.png")