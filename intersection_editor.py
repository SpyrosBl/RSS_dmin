import pandas as pd

# Read file
df = pd.read_csv('results_tracks_06.csv')  

# Add the header
df.columns = ['time', 'rear_car', 'front_car', 'RSS_dmin', 'driving_direction', 'Rear_Velocity', 'Actual_Euclidean_Distance', 'Intersection']

# Sort file according to time 
df.sort_values(['time'], axis = 0, ascending = [True], inplace = True)

# Select only the cases that the RSS Safe Longitudinal Distance is NOT kept and drop duplicates

# This dataframe contains all the interactions
final_df = df.drop_duplicates(subset = ['time','rear_car', 'front_car'], keep = 'first').reset_index(drop = True) 

# This dataset contains only those interactions where dmin is not held
rss_filtered_df = final_df[final_df['RSS_dmin'] > final_df['Actual_Euclidean_Distance']]

# Leave only the RSS dmin violation cases in the .csv file
rss_filtered_df.to_csv('results_tracks_19.csv', index = False)

# Show the driving direction where most RSS violations occur
driving_direction_df = rss_filtered_df['driving_direction'].value_counts()
print(driving_direction_df)

# Show how many RSS-Violations occur inside the intersection and main way 
intersection_df = rss_filtered_df['Intersection'].value_counts() 
print(intersection_df)

# Dataframe including RSS and Speed Limit Violations
filtered_speed_df = rss_filtered_df[rss_filtered_df['Rear_Velocity'] > 13.889] 
print('Number of speed limit Violations, when RSS dmin is already violated, is located in', filtered_speed_df['Intersection'].value_counts())
