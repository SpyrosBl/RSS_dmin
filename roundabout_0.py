import pandas as pd
import os
import csv
import itertools
import math

# assign and open dataset
file = 'C:/Users/Spyros/Desktop/Roundabouts/00_tracks.csv'
data = pd.read_csv(file, index_col = 'frame')

pwd = os.getcwd()
os.chdir(os.path.dirname(file))
trainData = pd.read_csv(os.path.basename(file))
os.chdir(pwd)

# Filter 1 - Sort data frame according to Time/Frames

data.sort_values(['frame'], axis=0, ascending=[True], inplace=True)
#print(len(data))

# Display sorted data frame
#print('\nAfter sorting:')
#print(data.tail(n = 2))

# Filter 2 - Heading Difference

def heading_difference(a, b):
    heading_diff = abs(a - b)
    if heading_diff < 10:
        return heading_diff
    else:
        pass

# Filter 3 - Distance between cars

def absolute_distance(a, b):
    abs_dist = (abs(a) - abs(b))**2
    return abs_dist

# Safe Longtitudinal Distance according to RSS-Paper

def safe_longitudinal_distance(vel_rear, vel_front, accel_max_rear):
    response_t = 1.0 # s
    min_brake = 6.43 # m/s^2 according to UNECE Rules
    max_brake = 11.0  # m/s^2
    dmin = (vel_rear * response_t) + (0.5 * accel_max_rear * (response_t**2)) + ((vel_rear + (response_t * accel_max_rear))**2 / (2 * min_brake)) - (((vel_front**2)/(2 * max_brake)))
    return float(dmin)

# Iterate over the frames
for frame in range(len(data)):
    frame_values = data.loc[frame]
    #print('The cars that are on the road on the same frame are' , cars, 'and they are %d in total ' %len(cars))

    # Create the Dataframe with the Second Filter - Heading
    # Since we do a pairwise comparison, we assign as Heading of 1st Vehicle = h1, Heading of 2nd Vehicle = h2
    for h1, h2 in itertools.combinations(frame_values['heading'], 2):
        heading_diff = heading_difference(h1, h2)
        heading_data = (h1, h2, heading_diff)

        if heading_diff is not None:
            heading_dataframe = frame_values.loc[frame_values['heading'] == heading_data[0]]
            heading_filtered_dataframe = heading_dataframe.append(frame_values.loc[frame_values['heading'] == heading_data[1]])
            #print('Dataframe filtered by heading difference is \n', heading_filtered_dataframe)
                                                                      
            # Create a csv file to store the results
            with open('results_tracks_00.csv', 'a', newline='') as outfile:

                # create the csv writer
                writer = csv.writer(outfile, delimiter=',')             
                
                # Access the Filtered Dataframe to check the Euclidean Distance, find the Rear, Front Vehicles and check if a safe distance is kept                              
                for car1, car2 in itertools.combinations(heading_filtered_dataframe['trackId'], 2):
                        for h1, h2 in itertools.combinations(heading_filtered_dataframe['heading'], 2):
                            for x1, x2 in itertools.combinations(heading_filtered_dataframe['xCenter'], 2):
                                for y1, y2 in itertools.combinations(heading_filtered_dataframe['yCenter'], 2):
                                    for u1, u2 in itertools.combinations(heading_filtered_dataframe['lonVelocity'], 2):
                                        for a1, a2 in itertools.combinations(heading_filtered_dataframe['lonAcceleration'], 2):
                                            time = frame                                                                                    
                                            car_datas = (car1, car2)
                                            heading_datas = (h1, h2)
                                            x_datas = (x1, x2)
                                            y_datas = (y1, y2)
                                            velocities = (u1, u2)
                                            accelerations = (a1, a2)
                                            xabs_dist = absolute_distance(x1, x2)
                                            yabs_dist = absolute_distance(y1, y2)
                                            euclidean_distance = math.sqrt(xabs_dist + yabs_dist)

                                            # Driving Direction Scenarios - Find Front and Rear Car and their dmin
                                            # The third filter of Euclidean Distance is implemented here directly
                                            if 1 < euclidean_distance < 30:
                                                # East = [0,45] & [ 315,360]
                                                if  0 < heading_datas[1] < 45 or 315 < heading_datas[1] < 360:
                                                    if x_datas[0] < x_datas[1]: # rear car is [0]
                                                        # check front car braking with rear acceleration RSS condition
                                                        if accelerations[1] < 0 and accelerations[0] > 0: # RSS braking front, accelerating rear car
                                                            d = (safe_longitudinal_distance(velocities[0], velocities[1], accelerations[0]))
                                                            res = [time, car_datas[0], car_datas[1], d, 'East',velocities[0],euclidean_distance]
                                                            # Check if rear car is in Roundabout, since rear vehicles are responsible for dmin violations
                                                            if -87 < y_datas[0] < -70 and 110 < x_datas[0] < 154 and -87 < y_datas[1] < -70 and 110 < x_datas[1] < 154:                                                         
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)
                                                        #print('Given Cars are moving East', heading_datas[1], 'and Rear car is:', car_datas[0])
                                                    elif x_datas[1] < x_datas[0]: # rear car is [1]                                                    
                                                        if accelerations[0] < 0 and accelerations[1] > 0: 
                                                            d = (safe_longitudinal_distance(velocities[1], velocities[0], accelerations[1]))
                                                            res = [time, car_datas[1], car_datas[0], d, 'East',velocities[1],euclidean_distance]
                                                            if -87 < y_datas[0] < -70 and 110 < x_datas[0] < 154 and -87 < y_datas[1] < -70 and 110 < x_datas[1] < 154: 
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)                                                
                                                        #print('Given Cars are moving East', heading_datas[1], 'and Rear car is:', car_datas[1])
    
                                                # North = [45, 135] - Data is given in negative Y!
                                                elif 45 < heading_datas[1] < 135:
                                                    if y_datas[1] < y_datas[0] : # rear car is [1]                                                   
                                                        if accelerations[0] < 0 and accelerations[1] > 0: 
                                                            d = (safe_longitudinal_distance(velocities[1], velocities[0], accelerations[1]))
                                                            res = [time, car_datas[1], car_datas[0], d, 'North',velocities[1],euclidean_distance]
                                                            if -67 < y_datas[0] < -103 and 125 < x_datas[0] < 130 and -67 < y_datas[1] < -103 and 125 < x_datas[1] < 130:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)
                                                        #print('Given Cars are moving North', heading_datas[1], 'and Rear car is:', car_datas[1])
                                                    elif y_datas[0] < y_datas[1] : # rear car is [0]                                                    
                                                        if accelerations[1] < 0 and accelerations[0] > 0:  
                                                            d = (safe_longitudinal_distance(velocities[0], velocities[1], accelerations[0]))
                                                            res = [time, car_datas[0], car_datas[1], d, 'North',velocities[0],euclidean_distance]
                                                            if -67 < y_datas[0] < -103 and 125 < x_datas[0] < 130 and -67 < y_datas[1] < -103 and 125 < x_datas[1] < 130:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)
                                                        #print('Given Cars are moving North', heading_datas[1], 'and Rear car is:', car_datas[0])
    
                                                # West = [135, 225] 
                                                elif 135 < heading_datas[1] < 225:
                                                    if x_datas[0] < x_datas[1]: # rear car is [1]                                                    
                                                        if accelerations[0] < 0 and accelerations[1] > 0:
                                                            d = (safe_longitudinal_distance(velocities[1], velocities[0], accelerations[1]))
                                                            res = [time, car_datas[1], car_datas[0], d, 'West',velocities[1],euclidean_distance]
                                                            if -87 < y_datas[0] < -70 and 110 < x_datas[0] < 154 and -87 < y_datas[1] < -70 and 110 < x_datas[1] < 154:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)                                                       
                                                            #print('Given Cars are moving West', heading_datas[1], 'and Rear car is:', car_datas[1], 'and their logitudinal distance is', d, 'at time point', time)
                                                    elif x_datas[1] < x_datas[0]: # rear car is [0]                                                    
                                                        if accelerations[1] < 0 and accelerations[0] > 0:
                                                            d = (safe_longitudinal_distance(velocities[0], velocities[1], accelerations[0]))
                                                            res = [time, car_datas[0], car_datas[1], d, 'West',velocities[0],euclidean_distance]
                                                            if -87 < y_datas[0] < -70 and 110 < x_datas[0] < 154 and -87 < y_datas[1] < -70 and 110 < x_datas[1] < 154:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)                                                        
                                                            #print('Given Cars are moving West', heading_datas[1], 'and Rear car is:', car_datas[0],'and their logitudinal distance is', d,'at time point', time)
    
                                                # South = [225, 315] - Data is given in negative Y! 
                                                elif 225 < heading_datas[1] < 315:
                                                    if y_datas[0] < y_datas[1]: # rear car is [1]  
                                                        if accelerations[0] < 0 and accelerations[1] > 0: 
                                                            d = (safe_longitudinal_distance(velocities[1], velocities[0], accelerations[1]))
                                                            res = [time, car_datas[1], car_datas[0], d, 'South',velocities[1],euclidean_distance]
                                                            if -67 < y_datas[0] < -103 and 125 < x_datas[0] < 130 and -67 < y_datas[1] < -103 and 125 < x_datas[1] < 130:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)
                                                        #print('Given Cars are moving South', heading_datas[1], 'and Rear car is:', car_datas[0])
                                                    elif y_datas[1] < y_datas[0]: # rear car is [0]  
                                                        if accelerations[1] < 0 and accelerations[0] > 0: 
                                                            d = (safe_longitudinal_distance(velocities[0], velocities[1], accelerations[0]))
                                                            res = [time, car_datas[0], car_datas[1], d, 'South',velocities[0],euclidean_distance]
                                                            if -67 < y_datas[0] < -103 and 125 < x_datas[0] < 130 and -67 < y_datas[1] < -103 and 125 < x_datas[1] < 130:
                                                                res.append('Roundabout')
                                                            else:
                                                                res.append('main way')
                                                            writer.writerow(res)                                                        
                                                        #print('Given Cars are moving South', heading_datas[1], 'and Rear car is:', car_datas[1])
                                                
                                                
                                