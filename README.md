# Astro-Coding-1221-Project-2
#### by Siena Baez, Xander Graves, Carrie Ries, and Alexis Walker

This is the 2nd project for Astro 1221, where we go over topics we have learned from Weeks 1 through 9.For our project 2, we are doing the Solar System Dashboard Project.

## Code Table of Contents 
### Imports and Prefaces: 
    Lines 1-26
### Solar System Information and Setup:
    Lines 27-136
### Plotting the Sky Paths: 
    Lines 137-281
### Conjunctions: 
    Lines 282-349
### Streamlit: 
    Lines 350-368


### Goal:
The objective of our project is to create a daily summary of all visible planets. This includes their positions, like their altitude and azimuth, as well as any future conjunctions. With this information, our code create graphs that models this information, and we have implemented a tool to let you choose the day in which the data displayed will be from. We will be using Skyfield and Pandas in order to achieve this goal.

### Methodology and Explanation: 
We started off by writing all the required imports we would need for our code to start running, such as numpy, pandas, matplotlib, and several astronomy related databases. We then set our default colors for our plots so that everything would show up affectively and clearly on them, and so that the graphs would look nicer overall. After the preliminary stuff, we started on getting all the data that we needed from the solar system bodies that we were going to include in our graphs and calculations. We did this by defining the place that will be where all the observations will be taken from, Columbus, and by grabbing the ephemeris files for all the planets in our solar system, as well as the ephemeris files for the sun and moon, that we put in a dictionary. We also created our time as a variable so that it can be changed for the days and hours we want it to and that will be chosen, and we made the time global so that it may be changed later in our streamlit page. 

The first thing we did with the data we collected was create code that would be able to tell the user what phase of the moon it will be during the chosen time. This takes the percentage of the moon illuminated in degrees--with 0 being new moon, 180 being full moon, and 360 being new moon again--and from that percentage labels which type of moon it will be at that night and stores it in a pandas dataframe. Next, we found the altitude and azimuth of each of the bodies in the dictionary we created with the ephemeris files and stored this in a pandas dataframe as well.

With the necessary information stored, we started on our plots. We made it so that, for each day, samples were taken at 15 minute incriments and there would be a total of 96 samples each day. The first plot we created was a graph that would show the daily polar sky paths of each of the solar system bodies in our dictionary. We started by defining the function that would allow us, with the altitude and azimuth we collected before, to plot these sky paths. We created a new time variable, t_day, that turns our time and the array of hours into Skyfield objects that the plot and functions used to get the information for the plot could use to get said information for whichever day is selected. We then created the parameters and colors for our graph, and grabbed the info about the altitude and azimuth that we needed. The way this plot is presented has it so that there are three distinct circles with a clear center and eight lines chunking the circles. The center of the circle is the zenith of the night sky and is represented by the 90 degrees. Then, each circle moving outwards goes down 30 degrees until the outermost circle, which is the horizon and is represented by the 0 degrees. The lines chunking the circles are then representing the cardinal directions of earth, where 0 degrees is North, 90 degrees is east, 180 is South, and 270 is West. This is so that you may clearly tell where each of the bodies are and in what way they are moving in the night sky from this plot. For our colors, we used the matplotlib "tableau 10" color map and made it so that each of the 10 bodies in our dictionary were assigned their own unique color that can be easily distinguished from the others. We also made sure to check if the bodies we are observing are below the horizon, and if they were we made a break. We then chunked the split arrays so they were still together. The holes that appear in some of the paths of the bodies on this plot are a result of gaps in the observation data, which can be seen and explained easier when they are shown on our second figure. And lastly, we made sure that whatever graph the code produces is saved as a png that will be displayed when the day is chosen on the streamlit.

Once the code for the first plot was finished, we started on making another graph to more clearly show how the altitude of the bodies in our dictionary changed throughout a 24 hour period. The process for making this graph was similar in many ways to the other, though we had to change multiple things to fit the different type of graph what we were plotting. We colored the bodies in the same way as the last graph, with the matplotlib "tableau 10" color map, and created another t_day time variable to use for pulling the information we need on the chosen day. The plot then differs from the first in that it is not a polar graph but a line graph showing the change in altitude for each of the bodies versus time in hours per day. We calculated the altitude through taking the bodies' apparent altitude from Columbus at t_day, making sure to account for atmospheric refraction, and turning that altitude into an array that can be plotted onto our graph. This data, along with the time and azimuth, are then put into our pandas dataframe. The graph then shows each of the bodies in different colors and their path above and below the horizon throughout the chosen 24 hour time period, and the gaps between all of the lines ending and the actual end of the graph is the gaps in observation data that was mentioned in the previous graph. I believe the issue was that the data at this time was not collected for whatever reason, and thus was not able to be graphed. The graph produced by the code on the chosen day is then again saved as a png to be displayed on streamlit.



### How to Run: 
1. Clone the repo: [git clone ...]
2. Install dependencies: [pip install -r requirements.txt]
3. Open the file 'Project_2_Streamlit.py"
4. Run the main script
5. Test out streamlit functions

### Disclaimer on AI Usage in Our Project: 
Though not used much at all throughout our project, AI was used in some minor areas where we were too confused to know what to do ourselves or needed help fixing the code when nothing else was working.