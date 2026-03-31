import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, wgs84
from skyfield import almanac
from datetime import datetime, timedelta, timezone
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
##All necessary imports for the project

plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['text.color'] = 'white'
plt.rcParams['figure.edgecolor'] = 'white'
plt.rcParams['legend.facecolor'] = "#0e1117"
#Setting default values for the plots to make them look nicer


eph = load('de440s.bsp')
ephemeris = eph 
#Using the de440s emphemeris file for the locations and later plotting

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
    "neptune": eph['neptune barycenter']
}
#Grabbing the planets from the emphemeris, putting them in a dictionary, and naming them
sun = eph['sun']
earth = eph['earth']
#for the moon phase calculations

ts = load.timescale()
#Skyfield's time system
hours = np.linspace(0, 24, 96)
global t_variable
t_variable = ts.utc(2026, 3, 1, hours + 7, 0)
t_start = ts.utc(2026, 3, 1)
t_end = ts.utc(2026, 3, 1 + 90)
#Singular day calculations and time variable for later use

columbus_lat = 39.9612
columbus_lon = -83.0003
columbus_elev = 260
#Location of Columbus, Ohio (observation point for our code)

columbus = earth + wgs84.latlon(columbus_lat, columbus_lon, elevation_m = columbus_elev)
#Creating the observer to call from


def moon_phase():

    
   percent_illuminated = 100 * columbus.at(t_variable).observe(eph['moon']).fraction_illuminated(eph['sun'])
    
   _, sunlong, _ = columbus.at(t_variable).observe(eph['sun']).apparent().frame_latlon(ecliptic_frame)
   _, moonlong, _ = columbus.at(t_variable).observe(eph['moon']).apparent().frame_latlon(ecliptic_frame)
   phase = (np.asarray(moonlong.degrees) - np.asarray(sunlong.degrees)) % 360
   #0 degrees is new moon, 90 degrees is first quarter, 180 degrees is full moon, 270 degrees is last quarter, and 360 degrees is new moon again
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




def observation_from_user(body, planet_name):

    astrometric = columbus.at(t_variable).observe(body)
    apparent = astrometric.apparent()
    alt, az, distance = apparent.altaz(pressure_mbar=1010)
    n = len(alt.degrees)
    df = pd.DataFrame({
        'Planet': [planet_name] * n,
        'Altitude': alt.degrees,
        'Azimuth': az.degrees,
    })
    return(df)
#gets the altitude and azimuth of the planets from the dictionary at the chosen time

for planet_name, body in bodies.items():
    df = observation_from_user(body, planet_name)
    print(planet_name)
    print(df)


def is_night(columbus_topos, single_day):
    night_check = almanac.dark_twilight_day(eph, columbus_topos)
    night_state = night_check(single_day)
    return night_state <= 1
#checks if it is night or not by checking if it is astronomical twilight. if it is less than 1, it is astronomical twilight

#Singular day calculations
global single_day
single_day = Time.now()

# Daily polar sky paths — run after the setup cell (needs `columbus`, `bodies`, `ts`).
N_SAMPLES_PER_DAY = 96  #samples in 15 minute increments throughout the day
def plot_all_planets_sky_path(year, month, day, n_samples=N_SAMPLES_PER_DAY):
    hours = np.linspace(0, 24, n_samples, endpoint=False) #ignores the last hour to avoid duplicates/overlap
    t_day = ts.utc(year, month, day, hours, 0)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar') #uses polar coordinates (degrees)
    ax.color = "black"
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 90)
    ax.set_yticks(range(0, 91, 30))
    ax.set_yticklabels(['90° Zenith', '60°', '30°', '0° (Horizon)'])
#setup for the polar plot that will show the daily sky paths of the planets
#90° Zenith is the top of the sky, 60° is 60 degrees above the horizon, 30° is 30 degrees above the horizon, and 0° (Horizon) is the horizon

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
            # Same tab10 color as plot_all_planets_altitude_vs_time for this planet
            color = tab[idx % len(tab)]
            mask_idx = np.where(mask)[0]
            # Split where visibility is not contiguous, so we do not draw
            # straight jump lines across below-horizon gaps.
            breaks = np.where(np.diff(mask_idx) > 1)[0] + 1
            chunks = np.split(mask_idx, breaks)

            legend_done = False
            az_rad = np.asarray(az.radians)
            for chunk in chunks:
                theta_chunk = az_rad[chunk]
                r_chunk = 90 - altd[chunk]

                # Handle Azimuth wrapping (0 <-> 360) to prevent cross-chart streaks
                wrap_breaks = np.where(np.abs(np.diff(theta_chunk)) > np.pi)[0] + 1
                theta_sub_chunks = np.split(theta_chunk, wrap_breaks)
                r_sub_chunks = np.split(r_chunk, wrap_breaks)

                for th, rr in zip(theta_sub_chunks, r_sub_chunks):
                    if len(th) < 2:
                        ax.plot(
                            th,
                            rr,
                            color=color,
                            marker='o',
                            markersize=3,
                            label=planet_name if not legend_done else None,
                        )
                    else:
                        ax.plot(
                            th,
                            rr,
                            color=color,
                            linewidth=2,
                            label=planet_name if not legend_done else None,
                        )
                    legend_done = True

    ax.legend(loc='upper left', bbox_to_anchor=(1.08, 1.02), fontsize=9)
    ax.set_title(f'All bodies sky paths — {year}-{month:02d}-{day:02d} UTC', pad=12)
    ax.set_thetagrids((0, 90, 180, 270), color="white")
    #0 is North, 180 is South
    plt.tight_layout()
    plt.show()
    plt.savefig("skypath.png") #saves the plot as a png file to later be displayed in streamlit
    return pd.concat(dfs, ignore_index=True)

# Single UTC day for sky paths
Y, M, D = 2026, 3, 1
day_key = f"{Y}-{M:02d}-{D:02d}"
sky_path_df = plot_all_planets_sky_path(Y, M, D).assign(UTC_date=day_key)
print(f"{day_key}: {len(sky_path_df)} rows")

def plot_all_planets_altitude_vs_time(year, month, day, n_samples=N_SAMPLES_PER_DAY):
    hours = np.linspace(0, 24, n_samples, endpoint=False)
    # Skyfield time array for each UTC hour
    # If this ever complains about float hours, use the t0 + seconds approach below instead.
    t_day = ts.utc(year, month, day, hours, 0)
    # t0 = ts.utc(year, month, day, 0, 0, 0)
    # t_day = t0 + hours * 3600
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
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
    ax.set_ylim(-90, 90)
    ax.set_xlabel("UTC Hour")
    ax.set_ylabel("Altitude (degrees)")
    ax.set_title(f"All bodies altitude vs time — {year}-{month:02d}-{day:02d} UTC")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=5)
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_xticklabels([0, 6, 12, 18, 24])
    ax.set_yticks((-90, 0, 90))
    ax.set_yticklabels([-90, '0 (Horizon)', 90])
    
    ax.set_yticks(range(-180, 181, 90))
    ax.set_yticklabels([-180, -90, '0 (Horizon)', 90, 180], color = 'white')
   #altitude vs time graph that shows the path of the planets throughout the entire day starting at noon EST

    plt.tight_layout()
    plt.show()
    plt.savefig("altvstime.png") #saves the plot as a png file to later be displayed in streamlit
    return pd.concat(dfs, ignore_index=True)

altitude_vs_time_df = plot_all_planets_altitude_vs_time(Y, M, D).assign(UTC_date=day_key)


close_threshold = 10.0  
step_minutes = 10

start_dt = datetime.datetime(2026, 3, 1, tzinfo=timezone.utc)
end_dt = datetime.datetime(2026, 5, 30, tzinfo=timezone.utc) 
step = timedelta(minutes=step_minutes)

n_steps = int((end_dt - start_dt) / step) + 1
_datetimes = [start_dt + i * step for i in range(n_steps)]
times_search = ts.from_datetimes(_datetimes)


def _refine_minimum_time(body_a, body_b, idx, samples=121):
    """Refine the minimum near times_search[idx] using a dense TT grid."""
    i0 = max(0, idx - 1)
    i1 = min(len(times_search) - 1, idx + 1)

    if i0 == i1:
        t_best = times_search[idx]
        sep_best = columbus.at(t_best).observe(body_a).apparent().separation_from(
            columbus.at(t_best).observe(body_b).apparent()
        ).degrees
        return t_best, float(sep_best)

    tt0 = times_search[i0].tt
    tt1 = times_search[i1].tt
    t_detail = ts.tt_jd(np.linspace(tt0, tt1, samples))

    a_pos = columbus.at(t_detail).observe(body_a).apparent()
    b_pos = columbus.at(t_detail).observe(body_b).apparent()
    seps = a_pos.separation_from(b_pos).degrees

    j = int(np.argmin(seps))
    return t_detail[j], float(seps[j])


def find_conjunctions_for_pair(name_a, body_a, name_b, body_b, close_threshold=close_threshold):
    a_pos = columbus.at(times_search).observe(body_a).apparent()
    b_pos = columbus.at(times_search).observe(body_b).apparent()
    seps = a_pos.separation_from(b_pos).degrees

    mins = np.where((seps[1:-1] < seps[:-2]) & (seps[1:-1] <= seps[2:]))[0] + 1
    mins = mins[seps[mins] < close_threshold]

    out = []
    for idx in mins:
        t_best, sep_best = _refine_minimum_time(body_a, body_b, idx)
        out.append(
            {
                "pair": (name_a, name_b),
                "time": t_best.utc_strftime("%Y-%m-%d %H:%M"),
                "separation_deg": float(sep_best),
            }
        )
    return out


names = list(bodies.keys())
all_conjunctions = []
for i, name_a in enumerate(names):
    for name_b in names[i + 1 :]:
        all_conjunctions.extend(
            find_conjunctions_for_pair(name_a, bodies[name_a], name_b, bodies[name_b])
        )

all_conjunctions = sorted(all_conjunctions, key=lambda d: (d["time"], d["pair"]))
conjunctions = pd.DataFrame(all_conjunctions)

#Streamlit app setup
st.title("Solar System Dashboard")
st.write("This Solar System Dashboard will track and display the positions of the planets (and the moon) in the sky in relation to Columbus, Ohio")
st.write("Select a date to see the positions of the planets in the sky")
DAYS_UTC = st.date_input("Select a date") #allows you to choose the date from a calendar that will display all the calculations and plots for that day 
if st.button("Plot Planets"):
    with st.spinner("Plotting planets..."):
        plot_all_planets_sky_path(DAYS_UTC.year, DAYS_UTC.month, DAYS_UTC.day)
        plot_all_planets_altitude_vs_time(DAYS_UTC.year, DAYS_UTC.month, DAYS_UTC.day)
        st.success("Planets plotted successfully!")
    col1, col2 = st.columns(2)
    col1.image("skypath.png")
    col2.image("altvstime.png")
    #plots the two saved images from earlier into streamlit
st.write("This prints conjunctions from March 1st 2026 to May 30th 2026")
if st.button("Print Conjunctions"):
    with st.spinner('Printing conjunctions...'):
        st.dataframe(conjunctions)
    #plots all the conjugations during the given time period