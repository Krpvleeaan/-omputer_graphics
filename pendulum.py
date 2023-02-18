import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.animation import ArtistAnimation
from matplotlib import animation
from PIL import Image
import matplotlib.lines as mlines

def bresenham(img, color, x1=0, y1=0, x2=0, y2=0):
    x1, y1, x2, y2 = y1, x1, y2, x2
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0: dx = -dx
    if dy < 0: dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0
    img[x, y] = color
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        img[x, y] = color

def nurbs_circle(p0: tuple, p1: tuple, p2: tuple, p3: tuple, centre, scale):
    w = 1/3
    count = 1000
    curve = list()
    step = 1/count
    index = 1/count
    for i in range(count):
        x = int((((1 - index)**3 * p0[0] + 3*index*(1 - index)**2*w * p1[0] + 3*index**2 * (1 - index)*w * p2[0] + index**3 * p3[0] ) / ((1-index)**3 + 3*index*(1-index)**2 * w + 3*index**2 * (1 - index) * w + index**3)) * scale + centre[0])
        y = int(((1 - index) ** 3 * p0[1] + 3 * index * (1 - index) ** 2 * w * p1[1] + 3 * index ** 2 * (1 - index) * w * p2[1] + index ** 3 * p3[1]) / ((1 - index) ** 3 + 3 * index * (1 - index) ** 2 * w + 3 * index ** 2 * (1 - index) * w + index ** 3) * scale + centre[1])
        curve.append((x, y))
        index+=step
    return curve

def print_curve_red(img, nurbs_points_right, nurbs_points_left):
    for i in range(len(nurbs_points_right)):
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][0] = 255
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][1] = 0
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][2] = 0

        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][0] = 255
        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][1] = 0
        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][2] = 0

def color_points_red(res_img, points_from, points_to):
    for i in range(len(points_from)):
        bresenham(res_img, [148,0,211], points_from[i][0], points_from[i][1], points_to[i][0], points_to[i][1])

def print_curve_blue(img, nurbs_points_right, nurbs_points_left):
    for i in range(len(nurbs_points_right)):
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][0] = 0
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][1] = 0
        img[nurbs_points_right[i][1]][nurbs_points_right[i][0]][2] = 255

        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][0] = 0
        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][1] = 0
        img[nurbs_points_left[i][1]][nurbs_points_left[i][0]][2] = 255

def color_points_blue(res_img, points_from, points_to):
    for i in range(len(points_from)):
        bresenham(res_img, [255,140,0], points_from[i][0], points_from[i][1], points_to[i][0], points_to[i][1])

if __name__ == '__main__':
    fig, ax = plt.subplots()
    size = 2048
    img = np.ones((size, size, 3), dtype = int) * [255,255,255]
    x0 = 1024
    y0 = 750
    radius = 600

    coord_of_points_for_moving = []
    for i in np.arange(0, np.pi, np.pi / 50):
        temp_x = x0 + radius * np.cos((i))
        temp_y = y0 + radius * np.sin((i))
        if (temp_y > 750):
            coord_of_points_for_moving.append((int(temp_x), int(temp_y)))
    quantity_of_points_for_moving = len(coord_of_points_for_moving)
    
    ims = []
    j = 0
    k = 0
    for i in range(int(quantity_of_points_for_moving / 2)):
        if (math.sqrt((coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][0]-coord_of_points_for_moving[i][0])**2)+((coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][1]-coord_of_points_for_moving[i][1])**2) > 300):
            res_img = np.copy(img)
            bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][0], coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][1])
            bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i][0], coord_of_points_for_moving[i][1])
            if (j < (quantity_of_points_for_moving / 2) / 2):
                points_right_move = nurbs_circle((0, 0), (26, 0), (26, -26 + j), (j, -26 + j), coord_of_points_for_moving[i], 6)
                points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, -26 + j), (-j, -26 + j), coord_of_points_for_moving[i], 6)
                points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
                points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
                j += 2
            else:   
                points_right_move = nurbs_circle((0, 0), (26, 0), (26, k), (26 - k, k), coord_of_points_for_moving[i], 6)
                points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, k), (-26 + k, k), coord_of_points_for_moving[i], 6)
                points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
                points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
                k += 2
            color_points_blue(res_img, points_right_stay, points_left_stay)
            color_points_red(res_img, points_right_move, points_left_move)
            print_curve_red(res_img, points_right_move, points_left_move)  
            print_curve_blue(res_img, points_right_stay, points_left_stay)
            im = ax.imshow(res_img, animated = True)
            ims.append([im])
        else:
            checkpoint = i + 1
            break

    for i in np.arange(checkpoint, int(quantity_of_points_for_moving /2 + 2), 1):
        res_img = np.copy(img)
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i - 1][0], coord_of_points_for_moving[i - 1][1])
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i + 3][0], coord_of_points_for_moving[i + 3][1])
        points_right_move_1 = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[i - 1], 6)
        points_left_move_1 = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[i - 1], 6)
        points_right_move_2 = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[i + 3], 6)
        points_left_move_2 = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[i + 3], 6)
        color_points_blue(res_img, points_right_move_1, points_left_move_1)
        color_points_red(res_img, points_right_move_2, points_left_move_2)    
        print_curve_blue(res_img, points_right_move_1, points_left_move_1)  
        print_curve_red(res_img, points_right_move_2, points_left_move_2)
        im = ax.imshow(res_img, animated = True)
        ims.append([im])

    checkpoint = int(quantity_of_points_for_moving /2) + 4
    j = 0
    k = 0
    
    for i in np.arange(checkpoint, quantity_of_points_for_moving - 2, 1):
        res_img = np.copy(img)
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][0], coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][1])
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i][0], coord_of_points_for_moving[i][1])
        if  (j < ((quantity_of_points_for_moving -1) - checkpoint) / 2):
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, 26 - j), (0 + j, 26 - j), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, 26 - j), (0 - j, 26 - j), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            j += 2
        else:
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, -k), (26 - k, -k), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, -k), (-26 + k, -k), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            k += 2
        color_points_blue(res_img, points_right_stay, points_left_stay)
        color_points_red(res_img, points_right_move, points_left_move)
        print_curve_red(res_img, points_right_move, points_left_move)  
        print_curve_blue(res_img, points_right_stay, points_left_stay)
        im = ax.imshow(res_img, animated = True)
        ims.append([im])

    checkpoint = quantity_of_points_for_moving - 2
    j = 0
    k = 0
    for i in np.arange(checkpoint, int(quantity_of_points_for_moving / 2 + 4), -1):
        res_img = np.copy(img)
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][0], coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][1])
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i][0], coord_of_points_for_moving[i][1])
        if (j < (checkpoint - int(quantity_of_points_for_moving / 2 + 3)) / 2):
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, -26 + j), (j, -26 + j), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, -26 + j), (-j, -26 + j), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            j += 2
        else:
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, k), (26 - k, k), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, k), (-26 + k, k), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            k += 2
        color_points_blue(res_img, points_right_stay, points_left_stay)
        color_points_red(res_img, points_right_move, points_left_move)
        print_curve_red(res_img, points_right_move, points_left_move)  
        print_curve_blue(res_img, points_right_stay, points_left_stay)
        im = ax.imshow(res_img, animated = True)
        ims.append([im])

    checkpoint = int(quantity_of_points_for_moving / 2)

    for i in np.arange(checkpoint, int(quantity_of_points_for_moving /2 - 4), -1):
        res_img = np.copy(img)
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i - 1][0], coord_of_points_for_moving[i - 1][1])
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i + 3][0], coord_of_points_for_moving[i + 3][1])
        points_right_move_1 = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[i - 1], 6)
        points_left_move_1 = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[i - 1], 6)
        points_right_move_2 = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[i + 3], 6)
        points_left_move_2 = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[i + 3], 6)
        color_points_red(res_img, points_right_move_1, points_left_move_1)
        color_points_blue(res_img, points_right_move_2, points_left_move_2)    
        print_curve_red(res_img, points_right_move_1, points_left_move_1)  
        print_curve_blue(res_img, points_right_move_2, points_left_move_2)
        im = ax.imshow(res_img, animated = True)
        ims.append([im])

    checkpoint = int(quantity_of_points_for_moving /2 - 4)
    k = 0
    j = 0
    for i in np.arange(checkpoint, 1, -1):
        res_img = np.copy(img)
        bresenham(res_img, 0, x0, y0, coord_of_points_for_moving[i][0], coord_of_points_for_moving[i][1])
        bresenham(res_img, 0, coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][0], coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)][1], x0, y0)
        if (j < (checkpoint) / 2):
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, 26 - j), (0 + j, 26 - j), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, 26 - j), (0 - j, 26 - j), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            j += 2
        else:
            points_right_move = nurbs_circle((0, 0), (26, 0), (26, -k), (26 - k, -k), coord_of_points_for_moving[i], 6)
            points_left_move = nurbs_circle((0, 0), (-26, 0), (-26, -k), (-26 + k, -k), coord_of_points_for_moving[i], 6)
            points_right_stay = nurbs_circle((0, 0), (26, 0), (26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            points_left_stay = nurbs_circle((0, 0), (-26, 0), (-26, 26), (0, 26), coord_of_points_for_moving[int(quantity_of_points_for_moving / 2)], 6)
            k += 2
        color_points_red(res_img, points_right_move, points_left_move)
        color_points_blue(res_img, points_right_stay, points_left_stay)    
        print_curve_red(res_img, points_right_move, points_left_move)  
        print_curve_blue(res_img, points_right_stay, points_left_stay)
        im = ax.imshow(res_img, animated = True)
        ims.append([im])
        
    ani = animation.ArtistAnimation(fig, ims, interval = 5, repeat = False, blit = True)
    writergif = animation.PillowWriter(fps = 12)
    ani.save('hw_4.gif', writer = writergif)