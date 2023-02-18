import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.animation import ArtistAnimation
from matplotlib import animation
from PIL import Image
import matplotlib.lines as mlines
import os
import imageio

def matr_rotation(x, y, step_to_circle):
    x = x - 250
    y = y - 250
    x_result = (x) * np.cos(step_to_circle) - (y) * np.sin(step_to_circle)
    y_result = (x) * np.sin(step_to_circle) + (y) * np.cos(step_to_circle)
    return (x_result + 250, y_result + 250)


def set_coord_of_points_in_circle(number_of_petals, radius, step_to_circle):
    coord_of_points_in_circle = []
    for i in range(number_of_petals):
        temp_x = x0 + radius * np.cos(step_to_circle * (i + 1))
        temp_y = y0 + radius * np.sin(step_to_circle * (i + 1))
        coord_of_points_in_circle.append((temp_x,temp_y))
    return coord_of_points_in_circle


def set_coord_of_points_distant_from_circle(number_of_petals, radius, step_to_circle):
    coord_of_points_distant_from_circle = []
    for i in range(number_of_petals):
        temp_x = x0 + (radius + radius + 30) * np.cos(step_to_circle * (i + 1))
        temp_y = y0 + (radius + radius + 30) * np.sin(step_to_circle * (i + 1))
        coord_of_points_distant_from_circle.append((temp_x,temp_y))
    return coord_of_points_distant_from_circle


def set_coord_of_mid_points_circle(number_of_petals, radius, step_to_circle):
    coord_of_mid_points_circle = []
    for i in range(number_of_petals):
        temp_x = x0 + (radius + radius/2) * np.cos((step_to_circle) * (i + 1))
        temp_y = y0 + (radius + radius/2) * np.sin((step_to_circle) * (i + 1))
        temp_x, temp_y = matr_rotation(temp_x , temp_y, step_to_circle/2)
        coord_of_mid_points_circle.append((temp_x, temp_y))
    return coord_of_mid_points_circle


def set_bezie_points(coord_of_points_in_circle, coord_of_mid_points_circle, coord_of_points_distant_from_circle):
    coord_of_left_bezie_points = []
    coord_of_right_bezie_points = []
    for idx, item in enumerate(coord_of_points_in_circle):
        for step in np.arange(0, 1, 0.01):
            res_x = (1 - step)**2 * item[0] + 2*step*(1 - step) * coord_of_mid_points_circle[idx][0] + step**2 * coord_of_points_distant_from_circle[idx][0]
            res_y = (1 - step)**2 * item[1] + 2*step*(1 - step) * coord_of_mid_points_circle[idx][1] + step**2 * coord_of_points_distant_from_circle[idx][1]
            coord_of_left_bezie_points.append((res_x, res_y))
    for idx, item in enumerate(coord_of_points_in_circle):
        for step in np.arange(0, 1, 0.01):
            res_x = (1 - step)**2 * item[0] + 2*step*(1 - step) * coord_of_mid_points_circle[idx - 1][0] + step**2 * coord_of_points_distant_from_circle[idx][0]
            res_y = (1 - step)**2 * item[1] + 2*step*(1 - step) * coord_of_mid_points_circle[idx - 1][1] + step**2 * coord_of_points_distant_from_circle[idx][1]
            coord_of_right_bezie_points.append((res_x, res_y))
    return coord_of_left_bezie_points, coord_of_right_bezie_points

def set_circle(x0, y0, radius):
    circle = []
    for i in range(500):
        for j in range(500):
            if ((i - x0) ** 2 + (j - y0) ** 2 <= radius ** 2):
                plt.plot(i, j, marker="o", markersize=1, markeredgecolor='yellow', markerfacecolor="yellow")
                circle.append((i , j))
    return circle

class Petal:
    
    def __init__(self, point_from , point_mid_left, point_mid_right, point_end):
        self.point_from = point_from
        self.point_mid_left = point_mid_left
        self.point_mid_right = point_mid_right
        self.point_end = point_end
        self.coord_of_left_bezie_points = []
        self.coord_of_right_bezie_points = []
        self.define_petal(point_from, point_mid_left, point_mid_right, point_end)

        
    def define_petal(self, point_from, point_mid_left, point_mid_right, point_end): #set bezie points
        left_bezie_points = []
        right_bezie_points = []
        for step in np.arange(0, 1, 0.01):
            res_x = (1 - step)**2 * point_from[0] + 2*step*(1 - step) * point_mid_left[0] + step**2 * point_end[0]
            res_y = (1 - step)**2 * point_from[1] + 2*step*(1 - step) * point_mid_left[1] + step**2 * point_end[1]
            left_bezie_points.append((res_x, res_y))
        for step in np.arange(0, 1, 0.01):
            res_x = (1 - step)**2 * point_from[0] + 2*step*(1 - step) * point_mid_right[0] + step**2 * point_end[0]
            res_y = (1 - step)**2 * point_from[1] + 2*step*(1 - step) * point_mid_right[1] + step**2 * point_end[1]
            right_bezie_points.append((res_x, res_y))
        self.coord_of_left_bezie_points = left_bezie_points
        self.coord_of_right_bezie_points = right_bezie_points
    

    def print_petal(self):
        for i in range(100):
            plt.plot(self.coord_of_left_bezie_points[i][0], self.coord_of_left_bezie_points[i][1], marker="o", markersize=1, markeredgecolor='white', markerfacecolor="white")
            plt.plot(self.coord_of_right_bezie_points[i][0], self.coord_of_right_bezie_points[i][1], marker="o", markersize=1, markeredgecolor='white', markerfacecolor="white")
            plt.plot([self.coord_of_left_bezie_points[i][0], self.coord_of_right_bezie_points[i][0]], [self.coord_of_left_bezie_points[i][1], self.coord_of_right_bezie_points[i][1]], 'white')
    

if __name__ == '__main__':
    fig, ax = plt.subplots()
    x0 = 250
    y0 = 250
    radius = 50


    number_of_petals = 6
    step_to_circle = np.radians(360 / number_of_petals)


    list_of_positions = []
    for rad in np.arange(0, 80, 20):
        list_of_petals = []
        coord_of_points_in_circle = set_coord_of_points_in_circle(number_of_petals, radius + rad / 3, step_to_circle)
        coord_of_points_distant_from_circle = set_coord_of_points_distant_from_circle(number_of_petals, radius + rad / 5, step_to_circle)
        coord_of_mid_points_circle = set_coord_of_mid_points_circle(number_of_petals, radius, step_to_circle)
        for i in range(number_of_petals):
            petal = Petal(coord_of_points_in_circle[i], coord_of_mid_points_circle[i], coord_of_mid_points_circle[i - 1], coord_of_points_distant_from_circle[i])
            list_of_petals.append(petal)
        list_of_positions.append(list_of_petals)

    for i in range(number_of_petals):
        for pos_petal in range(len(list_of_positions)):
            fig, ax = plt.subplots()        
            fig.set_size_inches(6,6)
            plt.axis([0, 500, 0, 500])
            ax.set_facecolor('black')
            circle = set_circle(x0, y0, radius)

            for j in range(i+1, number_of_petals):
                list_of_positions[0][j].print_petal()
            for j in range(0, i):
                list_of_positions[len(list_of_positions)-1][j].print_petal()
            list_of_positions[pos_petal][i].print_petal()
            plt.savefig(f'C:/Users/User/Desktop/Компьютерная графика/ЦВЕТЫ_6/{i}{pos_petal}')
            plt.close()
    path = 'C:/Users/User/Desktop/Компьютерная графика/ЦВЕТЫ_6/'
    frames = []
    for f in (os.listdir(path)):
        img = imageio.imread(path + f)
        frames.append(img)
    imageio.mimsave('flower6.gif',frames,fps = 5)