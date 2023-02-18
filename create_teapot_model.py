import re
import numpy as np
import matplotlib.pyplot as plt

Array_of_coord = []
Array_of_verges = []

def Scalar_Coord(x: int, y: int) -> tuple[int, int]:
    x0 = (x + p + 0.3) * size / (2 * (p + 0.3))
    y0 = (y + p + 0.3) * size / (2 * (p + 0.3))
    return int(x0), int(y0)

def create_img(background, kettle) -> list:
    for i in range(len(kettle)):
        for k in range(len(kettle[i])):
            if kettle[i][k] != [255, 255, 255]:
                kettle[i][k] = background[i][k]
    return kettle

def Bresenham(x0: int, y0: int, x1: int, y1: int, img: np.ndarray, teapot_color: np.ndarray, ) -> None:
    flag = 0
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    if x1 - x0 < y1 - y0:
        x0, y0, x1, y1 = y0, x0, y1, x1
        flag = 1
    if x1 - x0 < abs(y1 - y0):
        x0, y0, x1, y1 = y1, x1, y0, x0
        flag = 1
    error_rate = 0
    y = y0
    for x in range(x0, x1 + 1):
        if flag:
            img[y, x] = teapot_color
        else:
            img[x, y] = teapot_color
        error_rate = error_rate + abs(y1 - y0)
        if abs(x1 - x0) < error_rate * 2:
            if y1 > y0:
                y = y + 1
            else:
                y = y - 1
            error_rate = error_rate - abs(x1 - x0)


def Drawing(Array_of_coord, Array_of_veges, img, teapot_color) -> None:
    for f in Array_of_veges:
        for i in range(len(f)):
            x0, y0 = Scalar_Coord(*Array_of_coord[f[i - 1] - 1])
            x1, y1 = Scalar_Coord(*Array_of_coord[f[i] - 1])
            Bresenham(x0, y0 - 431, x1, y1 -431, img, teapot_color)

if __name__ == '__main__':
    with open("teapot.obj", 'r', encoding='utf-8') as file:
        for line in file:
            if line[0] == 'v':
                m = re.findall(r'[-]?\d\.\d*', line)
                del m[2]
                Array_of_coord.append(list(map(float, m)))
            if line[0] == 'f':
                m = re.findall(r'\d+', line)
                Array_of_verges.append(list(map(int, m))) 
    p = 0
    for v in Array_of_coord:
        for coord in v:
            if abs(coord) > p:
                p = abs(coord) 
    size = 2048
    teapot_img = np.zeros((size, size, 3), dtype=np.uint8)
    teapot_color = np.array([255, 255, 255], dtype=np.uint8)
    Drawing(Array_of_coord, Array_of_verges, teapot_img, teapot_color)
    teapot_img = np.rot90(teapot_img).tolist()


    Max_x = []
    Min_x =[]
    for j in range(len(teapot_img)):
        x_list = []
        for i in range(len(teapot_img)):
            if teapot_img[i][j] == [255,255,255]:
                x_list.append(j)
        if len(x_list) != 0:
            Max_x.append(max(x_list))
            Min_x.append(min(x_list))
    Max_width =  max(Max_x) -  min(Min_x)


    Max_y = []
    Min_y =[]
    for i in range(len(teapot_img)):
        y_list = []
        for j in range(len(teapot_img)):
            if teapot_img[i][j] == [255,255,255]:
                y_list.append(i)
        if len(y_list) != 0:
            Max_y.append(max(y_list))
            Min_y.append(min(y_list))
    Max_height=  max(Max_y) -  min(Min_y)


    Min_length = min(Max_height,Max_width)
    grad = np.zeros((size,size,3), dtype=np.uint8)
    Inner = (255, 0, 0)
    Outer = (0,0,255)
    for y in range(Min_length):
        for x in range(Min_length):
            Radius = np.sqrt((x - Min_length/2) ** 2 + (y - Min_length/2) ** 2)
            Radius = Radius / (Min_length/2)
            r = Outer[0] * Radius  + Inner[0] * (1 - Radius)
            g = Outer[1] * Radius  + Inner[1] * (1 - Radius)
            b = Outer[2] * Radius  + Inner[2] * (1 - Radius)
            if (Min_length/2)**2 >=  ((x  - Min_length/2)**2 +  (y  - Min_length/2)**2):
                grad[y + size//2 - Min_length//2, x  + size//2 - Min_length//2] = (int(r), int(g), int(b))
    Result = create_img(grad,teapot_img)
    plt.imshow(Result)
    plt.savefig("hw2_karpov_artem_09-041.png")
    plt.show()