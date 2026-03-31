# Astro-Coding-1221-Project-2
#### by Siena Baez, Xander Graves, Carrie Ries, and Alexis Walker

This is the 2nd project for Astro 1221, where we go over topics we have learned from Weeks 1 through 9.For our project 2, we are doing the Solar System Dashboard Project.

## Table of Contents 
### Imports and Prefaces: 
    Lines 1-26
### Solar System Information and Setup:
    Lines 27-136
### Plotting the Sky Paths and Conjunctions: 
    Lines 136-345
### Streamlit: 
    Lines 346-360


### Goal:
The objective of our project is to create a daily summary of all visible planets. This includes their positions, like their altitude and azimuth, as well as any future conjunctions. With this information, our code create graphs that models this information, and we have implemented a tool to let you choose the day in which the data displayed will be from. We will be using Skyfield and Pandas in order to achieve this goal.

### Methodology: 
We started off by writing all the required imports we would need for our code to start running, such as numpy, pandas, matplotlib, and several astronomy related databases. We then set our default colors for our plots so that everything would show up affectively and clearly on them, and so that the graphs would look nicer overall. After the preliminary stuff, we started on getting all the data that we needed from the solar system bodies that we were going to include in our graphs and calculations. We did this by defining the place that will be where all the observations will be taken from, Columbus, and by grabbing the ephemeris files for all the planets in our solar system, as well as the ephemeris files for the sun and moon, that we put in a dictionary. We also created our time as a variable so that it can be changed for the days and hours we want it to and that will be chosen, and we made the time global so that it may be changed later in our streamlit page. 

The first thing we did with the data we collected was create code that would be able to tell the user what phase of the moon it will be during the chosen time. This takes the percentage of the moon illuminated in degrees--with 0 being new moon, 180 being full moon, and 360 being new moon again--and from that percentage labels which type of moon it will be at that night and stores it in a pandas dataframe. Next, we found the altitude and azimuth of 

### How to Run: 
1. Clone the repo: [git clone ...]
2. Install dependencies: [pip install -r requirements.txt]
3. Run the main script
4. Test out streamlit functions





Create a comprehensive daily summary of all visible planets, their positions, and upcoming conjunctions. The challenge is using 
Skyfield to compute positions for all solar system objects while organizing the results in Pandas for easy querying and visualization.

Astronomy Context: A "conjunction" occurs when two planets appear very close together in the sky—a beautiful sight through telescopes. 
"Elongation" is the angular separation between a planet and the Sun (important for Mercury/Venus which are only visible near 
sunrise/sunset). "Retrograde motion" is when a planet appears to move backwards relative to background stars—an illusion caused 
by Earth's orbital motion. "Opposition" is when an outer planet is directly opposite the Sun in the sky—the best time to observe it 
(highest, brightest, closest to Earth).

Use Skyfield to calculate Sun, Moon, and planet positions for each day (Skyfield provides functions for all these calculations), 
store in a multi-index DataFrame (date, object), compute rise/set times and culmination with Astropy, identify conjunctions by 
detecting when planets are within X degrees (you can use angular separation functions from Astropy). Use Pandas to find tonight's 
visible planets (above horizon after sunset), determine best viewing times (highest altitude), and track planet motion through 
constellations. Create visualizations showing planet tracks across the sky, elongation from Sun over time, and upcoming conjunction 
dates. Generate "what's up tonight" reports with formatted tables.

The minimal version computes positions for 8 planets plus Moon over 30 days, identifies visible planets each evening, 
finds 2+ conjunctions in the period, creates a simple sky position plot, and generates a nightly observing report. 
Advanced versions might calculate planet brightness and apparent size, identify greatest elongations for Mercury/Venus, 
predict occultations, create animated sky movies showing planet motion, compute retrograde periods, track opposition dates 
for outer planets, or build a "planet observing challenge" system.