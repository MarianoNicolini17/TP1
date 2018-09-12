import numpy as np

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


point1 = np.array([1, 1])
point2 = np.array([-1, 1])
point3 = np.array([-1, -1])
point4 = np.array([1, -1])

old_x = (point1[0], point2[0], point3[0], point4[0])
old_y = (point1[1], point2[1], point3[1], point4[1])

old_area = PolyArea(old_x, old_y)

matrix = np.matrix([[1, 1], [1, 1]])

new_point1 = np.dot(matrix, point1)
new_point2 = np.dot(matrix, point2)
new_point3 = np.dot(matrix, point3)
new_point4 = np.dot(matrix, point4)

new_x = (new_point1.item(0), new_point2.item(0), new_point3.item(0), new_point4.item(0))
new_y = (new_point1.item(1), new_point2.item(1), new_point3.item(1), new_point4.item(1))

new_area = PolyArea(new_x, new_y)
print(new_area)
print(np.linalg.det(matrix))