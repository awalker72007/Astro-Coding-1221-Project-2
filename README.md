# Astro-Coding-1221-Project-2
## by Siena Baez, Xander Graves, Carrie Ries, and Alexis Walker

This is the 2nd project for Astro 1221, where we go over topics we have learned from Weeks 1 through 9.For our project 2, we are doing the Solar System Dashboard Project.
### Goal:
The goal is to create a daily summary of all visible planets. This will also include their positions, as well as any future conjunctions.
We will be using Skyfield and Pandas in order to achieve this goal.

First, 








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