# Astro-Coding-1221-Project-2
#### by Siena Baez, Xander Graves, Carrie Ries, and Alexis Walker

This is the 2nd project for Astro 1221, where we go over topics we have learned from Weeks 1 through 9.For our project 2, we are doing the Solar System Dashboard Project.

## Table of Contents 
### Imports and Prefaces: 
    Lines 1-26
### Solar System Information and Setup:
    Lines 27-136
### Plotting the Sky Paths and Conjunctions: 
    Lines 137-348
### Streamlit: 
    Lines 349-367


### Goal:
The objective of our project is to create a daily summary of all visible planets. This includes their positions, like their altitude and azimuth, as well as any future conjunctions. With this information, our code create graphs that models this information, and we have implemented a tool to let you choose the day in which the data displayed will be from. We will be using Skyfield and Pandas in order to achieve this goal.

### Methodology: 
We started off by writing all the required imports we would need for our code to start running, such as numpy, pandas, matplotlib, and several astronomy related databases. We then set our default colors for our plots so that everything would show up affectively and clearly on them, and so that the graphs would look nicer overall. After the preliminary stuff, we started on getting all the data that we needed from the solar system bodies that we were going to include in our graphs and calculations. We did this by defining the place that will be where all the observations will be taken from, Columbus, and by grabbing the ephemeris files for all the planets in our solar system, as well as the ephemeris files for the sun and moon, that we put in a dictionary. We also created our time as a variable so that it can be changed for the days and hours we want it to and that will be chosen, and we made the time global so that it may be changed later in our streamlit page. 

The first thing we did with the data we collected was create code that would be able to tell the user what phase of the moon it will be during the chosen time. This takes the percentage of the moon illuminated in degrees--with 0 being new moon, 180 being full moon, and 360 being new moon again--and from that percentage labels which type of moon it will be at that night and stores it in a pandas dataframe. Next, we found the altitude and azimuth of each of the bodies in the dictionary we created with the ephemeris files.

With the necessary information stored, we started on our plots. We made it so that, for each day, samples were taken at 15 minute incriments and there would be a total of 96 samples each day. 

### How to Run: 
1. Clone the repo: [git clone ...]
2. Install dependencies: [pip install -r requirements.txt]
3. Open the file 'Project_2_Streamlit.py"
4. Run the main script
5. Test out streamlit functions

### Disclaimer on AI usage: 
Though not used much at all throughout our project, AI was used in some minor areas where we were too confused to know what to do ourselves or needed help fixing the code when nothing else was working.