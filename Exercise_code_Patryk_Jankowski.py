import os
import numpy as np
import matplotlib.pyplot as plt
import statistics

#load folder with data
all_files = os.listdir('Data')

#start plotting figure 1 - greyed out comparison figure
plt.figure()
plt.title("Amplification vs Frequency")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Amplification [Mag]')
plt.xlim(left = 100, right = 560)
plt.ylim(top = 880, bottom  = 700)
#define initial arrays

#array with sum of all the measurements
data_sum = 0

#main data array from .csv files
data = 0

#array of maximal values of amplification for a given frequency
data_max = np.empty((2001,))

#array of minimal values of amplification for a given frequency
data_min = np.loadtxt(os.path.join('Data', "Chan_5.csv"),skiprows=7,delimiter=',')
data_min = data_min[:,5]

#main iteration variable
i = 0

#array for initial data for standard deviation calculation
std_data_array = np.array([])

#loop through all the files in "Data"
for one_file in all_files:
    
    data = np.loadtxt(os.path.join('Data', one_file),skiprows=7,delimiter=',')
    
    #extract frequency (xdata) and magnityde (ydata)
    xdata = data[:,0]/1e6
    ydata = data[:,5]
    
    plt.plot(xdata,ydata, color="#808080")
    
    #calculate data sum
    data_sum = data_sum + ydata
    i = i + 1
    z = 0

    #append the standard deviation data array
    if i-1 == 0:
        std_data_array = ydata
    else:
        std_data_array = np.append(std_data_array, ydata)
    
    #add max and min valyes to max and min data arrays    
    for u in ydata:
        
        if u >= data_max[z]:
            data_max[z] = u
        
        if u < data_min[z]:
            data_min[z] = u
            
        z = z + 1

plt.fill_between(xdata, data_max, data_min, color="#C0C0C0")

#calculate array of average ydata
data_average = data_sum/i

plt.plot(xdata, data_average, "k-")

#plot overwiew figure
plt.figure()
plt.title("Amplification vs Frequency - overview")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Amplification [Mag]')
plt.plot(xdata, data_average, "k-")
#plt.plot(xdata, data_max, "r-")
#plt.plot(xdata, data_min, "b-")
plt.fill_between(xdata, data_max, data_min, color="#C0C0C0")


#calculate standard deviation for each frequency measurement
std_multiD_array = np.split(std_data_array, i)
std = np.std(std_multiD_array, axis=0, dtype=np.float64)

#calculate absolute and relative "error" (difference between measurements)
abs_error = abs((data_max - data_min)/2)
rel_error = abs_error/data_average*100

#plt.figure()
#plt.plot(xdata, abs_error, "r-")
#plt.plot(xdata, std, "b-")

#plot relative "error" figure
plt.figure()
plt.title("Relative measurement difference vs Frequency")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Relative measurement difference (%)')
plt.plot(xdata, rel_error, "go", markersize=3)

#same plot but truncated
plt.figure()
plt.title("Relative measurement difference vs Frequency")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Relative measurement difference (%)')
plt.xlim(left = 39, right = 700)
plt.ylim(top = 10, bottom  = 0)
plt.plot(xdata, rel_error, "go", markersize=3)

#count data lying within 1 standard deviation (i_std) and 3 standard deviations (iii_std) 
i_std = 0
iii_std = 0

for one_file in all_files:
    data = np.loadtxt(os.path.join('Data', one_file),skiprows=7,delimiter=',')
    ydata = data[:,5]
    z = 0
    for u in ydata:
        if u <= data_average[z]+std[z] and u >= data_average[z] - std[z]:
            i_std = i_std + 1
        
        if u <= data_average[z]+ 3*std[z] and u >= data_average[z]- 3*std[z]:
            iii_std = iii_std + 1
        
        z = z + 1

#calculate the percentage of measurements falling within 1 and 3 standard deviations of average data
percent_i_std = i_std/(i*len(ydata))*100
percent_iii_std = iii_std/(i*len(ydata))*100

#plot figure of average data with indication of 1 standard deviation area between the red and blue curves compared to greyed out area of max and min measurements
plt.figure()
plt.title("Amplification vs Frequency - standard deviation")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Amplification [Mag]')
plt.plot(xdata, data_average, "k-")
plt.plot(xdata, data_average + std, "r-")
plt.plot(xdata, data_average-std, "b-")
#plt.plot(xdata, data_max, "g-")
#plt.plot(xdata, data_min, "m-")
plt.fill_between(xdata, data_max, data_min, color="#C0C0C0")
plt.show()