# Clustering
Clustering coordinates based on distance


The idea behind this script, is that it finds the least amount of cluster points, that contains all the supplied coordinates.

This is my first ever GitHub post, and first ever full python script.
The script is VERY rough, and not very user friendly, as it was made for personal use, and was not intended to be shared.
Please feal free to make recommendations or ways to clean up the script :)

NOTE: 
LatDegPerMeter = 0.000008999
LongDegPerMeter = 0.000010844

The above variables are calculated for South Africa, it is how many degrees per meter for latitude and longatude.
For sake of accuracy, I advise doing the calculation for your region.
If you know how to automate this, you can add it in.

I hope you get some use out of it.



It creates a final clustered list as follows:

1. Generates thousands of "Circles" that cover the entire area with a spacing specified using "meters = "
	1.1 Note that every time the "meters" perameter is halved, the database generated is multiplied by 4 (Thanks math)
	1.2 Note that RAM usage gets extremely high when using any value < 10
2. Calculates distances between all circles created and coordinates provided.
3. Creates a distance table, using Pandas Dataframe to house the data.
4. Removes all coordinates that distance are > 70m.
5. Countes number of nearby coordinates for each circle.
6. Sort circles by number of nearby coordinates
7. Remove all circles that contain 0 coordinates within 70m
8. Runs a loop to create the final database of clustered coordinates by doing the following:
	8.1 Count number of nearby coordinates
	8.2 Remove all circles with 0 nearby coordinates
	8.3 Sort table by number of nearby coordinates
	8.4 Add largest circle (most coordinates nearby) to final list
	8.5 Remove all coordinates within largest circle from database
	8.6 Remove largest circle from database
	8.7 Start from 8.1 again using new filtered coordinate database
	The above loop adds 1 circle to the final list each loop, multiple circles are removed from the database per loop, depending on the coordinates removed.
9. Save the final list of circles to a file called "Clustered_Spawnpoints.txt"



How to use:

1. Add list of coordinates that require clustering to "Pokestops.csv"
	1.1 Note i have included some coordinates to show formatting
2. Decide on the "Meteres = " value, recommended > 10 as you get diminishin returns below 10m
3. Change clustering distance if needed, default is 70m (This is ideal range for Pokemon Go, which this was made for)
4. Run the "stack.py" script, it will output a file called "Clustered_Spawnpoints.txt" which will contain all clusterd coordinates.
	4.1 The list of clusters will be in order from "Most points in cluster to least"
