# Package imports

import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import random
import copy


# Plot Class for containing elevation data talbe

os.chdir('C:\\Users\\charl\\MathModeling\\IM2C')


class Plot:

    # Constructor for Plot
    def __init__(self, shape, elevations):
        self.shape = shape
        self.elevations = np.array(elevations)

    # Convert to string default method
    def __str__(self):
        print(f"Shape {self.shape} sized plot")

# Subclass SubPlot is a Plot, this is the window


dely = 0.174
delx = 0.174

# Sub plot subclass for getting sub window given x range and y range


class SubPlot(Plot):

    # Constructor for SubPlot

    def __init__(self, *args, x_range, y_range, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_range = x_range
        self.y_range = y_range
        self.grads = None

    # Returns pixel classification array with ranges and elevation array with ranges
    def get_plot_section(self):
        return self.elevations[self.y_range[0]:self.y_range[1], self.x_range[0]:self.x_range[1]]

    # Get gradients based on elevation array

    def get_grads(self):
        elev = self.get_plot_section()
        self.grads = copy.deepcopy(elev)
        for row in range(1, len(elev)-1):
            for col in range(1, len(elev[0])-1):

                # Gradient from the left coordinate
                left_grad = abs(elev[row][col-1] -
                                elev[row][col]) / (delx)

                # Gradient from the right coordinate
                right_grad = abs(elev[row][col+1] -
                                 elev[row][col]) / (delx)

                # Gradient from the top coordinate
                top_grad = abs(elev[row+1][col] -
                               elev[row][col]) / (dely)

                # Gradient from the below coordinate
                bot_grad = abs(elev[row-1][col] -
                               elev[row][col]) / (dely)

                # Sum gradients
                sum_grad = left_grad + right_grad + top_grad + bot_grad
                self.grads[row][col] = sum_grad / 4

        return self.grads[1:-1, 1:-1]

    # Return mean of the array of the gradients
    def avg_grad(self):
        return np.mean(self.get_grads())

    # Calculate total surface area
    def surface_area(self):
        total_area = 0

        # Loop over all gradients to calculate new side length
        for row in range(len(self.grads)):
            for col in range(len(self.grads[0])):
                # calculate side lengths

                # x_side length
                x_side = np.sqrt(delx ** 2 + self.grads[row][col] ** 2)

                # y_side length
                y_side = np.sqrt(dely ** 2 + self.grads[row][col] ** 2)
                total_area += x_side * y_side

        # return total area
        return total_area


# Find elevations from table
# elevations = [[random.random() / 100 for i in range(16)] for j in range(16)]

# # Initialize Subplot object
# plot = SubPlot((len(elevations), len(
#     elevations[0])), elevations=elevations,  x_range=[0, 16], y_range=[0, 16])

# # Get specific plot section and load variables
# plot2 = plot.get_plot_section()

# Testing print statements
# print(plot2)
# print(plot.get_grads())
# print(plot.avg_grad())
# print(plot.surface_area())

# Params: elevations=elevation table, x_partitions = num of x axis partitions, y_partitions = num y axis partitions

# Calculate all necessary components for the topological factors section
def calculate_all_topological_factors(elevations, x_partitions, y_partitions):

    #define some variables
    x_max = len(elevations[0])
    y_max = len(elevations[1])
    x_ranges = []
    y_ranges = []

    #if we do not partition along the x axis...
    if x_partitions == 0:
        x_len = 0
        x_ranges.append([0, x_max])
    else:
        assert x_max % x_partitions == 0
        x_len = int(x_max / x_partitions)

    #if we do not partition along the y axis...
    if y_partitions == 0:
        y_len = 0
        y_ranges.append([0, y_max])
    else:
        assert y_max % y_partitions == 0
        y_len = int(y_max / y_partitions)

    # create x_ranges variable
    for i in range(x_partitions):
        x_ranges.append([i*x_len, (i+1)*x_len])

    # create y_ranges variable
    for i in range(y_partitions):
        y_ranges.append([i*y_len, (i+1)*y_len])

    # loop over each x_range and y_range and create subplot and calculate values
    for x_range in x_ranges:
        for y_range in y_ranges:
            plot = SubPlot((len(elevations), len(
                elevations[0])), elevations=elevations, x_range=x_range, y_range=y_range)
            average_gradient = plot.avg_grad()
            surface_area = plot.surface_area()

            # print it out nicely
            print("___________________________________")
            print(f"X: {x_range[0]} --> {x_range[1]}")
            print(f"Y: {y_range[0]} --> {y_range[1]}")
            print(f"Surface Area: {surface_area}")
            print(f"Avg Elevation Change: {average_gradient}")


#elevations = [[random.random() / 100 for i in range(16)] for j in range(16)]
#calculate_all_topological_factors(elevations, 4, 2)

elevations = []

#data preprocessing step
with open('points_xyz.csv', 'r') as f:
    row = []
    counter = 0
    
    for line in f.readlines():
        row.append(float(line[-8:]) / 1000)
        counter += 1
        if len(row) % 16 == 0:
            elevations.append(row)
            row = []

with open('elevations.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerows(elevations)

elevations = np.array(elevations)

x_partitions = 0 #INPUT VALUE HERE
y_partitions = 0 #INPUT VALUES HERE

calculate_all_topological_factors(elevations, x_partitions, y_partitions)