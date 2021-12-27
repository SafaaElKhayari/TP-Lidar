import numpy as np
import math as m
import pandas as pd


# bras de levier & matrice de rotation
bras_levier = [0.14, 0.249, -0.076]
# matrice de rotation
matrice_rotation = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]

fake_data = [[12, 0, 3.2141, 0.6925, 66.8928, 255.0, 255.0, 255.0],
             [13, 0, 3.5502, 0.6937, 66.8767, 255.0, 255.0, 255.0],
             [12, 0, 3.2141, 0.6925, 66.8928, 255.0, 255.0, 255.0],
             [15, 0, 4.2221, 0.6961, 66.8369, 255.0, 255.0, 255.0],
             [5376, 499, -0.1022, -0.0030, -0.2184, 86.0, 86.0, 86.0]]

np_data = np.array(fake_data)

# matrix of rotation


def Rx(theta):
    return np.matrix([[1, 0, 0],
                     [0, m.cos(theta), -m.sin(theta)],
                     [0, m.sin(theta), m.cos(theta)]])


def Ry(theta):
    return np.matrix([[m.cos(theta), 0, m.sin(theta)],
                     [0, 1, 0],
                     [-m.sin(theta), 0, m.cos(theta)]])


def Rz(theta):
    return np.matrix([[m.cos(theta), -m.sin(theta), 0],
                     [m.sin(theta), m.cos(theta), 0],
                     [0, 0, 1]])

# main function


def convert_to_cart_coord(GPS_data, scanner_data):
    rotation_matrix = Rx(scanner_data[:, 5]) * \
        Ry(scanner_data[:, 6]) * Rz(scanner_data[:, 7])

    coord = GPS_data[:, 2:5] + rotation_matrix * \
        (bras_levier + matrice_rotation * scanner_data[:, 2:5])

    return coord


# Random 3 points
def random_points(data):
    data_coord = data[:, 2:5]
    number_of_rows = data_coord.shape[0]
    random_indices = np.random.choice(number_of_rows, size=3, replace=False)
    random_rows = data_coord[random_indices, :]
    return random_rows


# test results
result = random_points(np_data)
print(result)


# collinearity

def Test_Collinearity(pts):
    # vectors
    v1 = pts[1] - pts[0]
    v2 = pts[2] - pts[0]
    # scalar product
    P = np.dot(v1, v2)
    # norms :
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    # alpha
    alpha = round(m.acos(P/(n1*n2), 4))
    # test collinearity
    if (m.isclose(alpha, 0)):
        return False

    return True
