# Readme File

#### This readme file explains the Code and the philosophy used in the research of RSS - Longitudinal Safe Distance for agents that drive on the same direction. It applies this particular RSS rule in Intersection and Roundabout scerarios, provided by the inD and rounD Datasets of RWTH Aachen. 

<br />

## General

### Goal
#### Goal of this research is to check how many of the traffic users obey to the RSS rule of longitudinal safe distance and extract valuable information about the violation percentages, their whearebouts and possible speed limit breach.

<br />

## Methodology

<br />

### intersection_XX.py and roundabout_XX.py files
#### The methodology used for both datasets is similar.

<br />

### First Filter
#### At first an extraction of the pairs that use the road at the same time is needed .The datasets provided are sorted according to agents and traffic users. Therefore, they are first sorted according to time. This allows a pairwise comparison of traffic users that occuppy the road at the same time. 

<br />

### Second Filter
#### The research targets agents that have the same direction while using the road. This is applied by taking only those agents with the same Heading Value +- a deviation of 10 degrees (the values set are the researcher's Initiative). Subsequantly a pairwise grouping of the traffic agents is made. They form a "Heading Filtered Dataframe". This was made possible with the command:
```Python
 itertools.combinations(frame_values['heading'], 2):
 ``` 
 <br />

### Third Filter
#### By accesing the "Heading Filtered Dataframe" an extraction of agents  that have an Euclidean Distance between 1m and 30m is made. The 1m threshold is used to avoid agents that drive side-to-side, in parallel with each other and ensure a front-rear vehicle situation (the values set are the researcher's Initiative). While using again the command:
```Python
 itertools.combinations(heading_filtered_dataframe['wanted_column'], 2): 
 ```  
#### it was able to extract all the RSS relevant information: frame,vehicle_id, velocity, acceleration and position for both agents. Optional: as with the second filter, a "Distance Filtered Dataframe" can also be made. It was omitted in the final version of the code for performance reasons.

<br />

### Front - Rear Vehicle
#### The datasets do not provide information on which agents is front or rear. By using the heading and positional values as well as, the dataset information found on the inD and rounD websites, this information could be obtained.

<br />

### Calculation of Longitudinal Safe Distance *dmin*
#### After the filtering, the calculation of the minimum safe distance between road agents with the same direction could be made. This was set in the 
```Python
 def safe_longitudinal_distance(vel_rear, vel_front, accel_max_rear): 
 ```  
#### function with some of the values being constant. Then for various values of Response Time ρ and Maximum Braking of Front vehicle, the results were derived. All the values used in this function were based on earlier research papers and the RSS papers.

<br />

### Position and direction
#### According to the coordinates of the vehicles and with the help of the inD Python Dtataset tools the boundaries of the Intersections and Roundabouts could be found. If both agents are inside those boundaries their position is marked with *Intersection/Roundabout*, else with *main way*. With the heading values, the direction of the agents was derived.

<br />

### Results
#### The results were saved in a results_ZZ.csv file that contain in a single line the following: front agent, rear agent, *dmin* , actual euclidean distance, direction and position. An example can be seen below:
```csv
time,rear_car,front_car,RSS_dmin,driving_direction,Rear_Velocity,Actual_Euclidean_Distance,Intersection
9,2,3,21.83138549909255,Southwest,9.6474,21.738943291441284,main way
10,5,8,25.99762518492929,Southwest,12.74616,21.408787153664264,Intersection
```
<br />

### intersection_editor.py and roundabout_editor.py files
#### These files were made to make the extraction of information easier. It removes duplicate values and filters the results_ZZ.csv file created in the main files. It helps find out how many RSS *dmin* violations occur and where, the direction of the agents that violate the safe longitudinal distance as well as, how many speed limit violations are found in each case, while the *dmin* is not held.

<br />

#### Aknowlegdments
##### This code was developed by Spyridon Bellias and was first used in his Master Thesis which was part of a greater research on RSS rules under the auspicies of the Karlsruhe Institute of Technology (KIT), the Institute of Measurement and Control Systems of KIT (MRT) and the Research Center of Information Technology in Karlsruhe (FZI). Please cite or refer to this work if you use it for further research.