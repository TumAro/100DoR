from math import sin, cos
import numpy as np

class Transformation3D:
    def __init__(self):
        self.dim = 4
        self.M = np.identity(self.dim, float)

    def _reset(self):
        self.M = np.identity(self.dim, float)

    def _getPos(self):
        pos = self.M[:3, -1]
        return pos.tolist()
    
    def _get_transform_mat(self, array=True):
        if not array:
            mat = self.M
            return mat.tolist()
        else:
            return self.M

    def __rotInit__(self, angle):
        rot_matrix = np.array([
            [cos(angle), -sin(angle)],
            [sin(angle), cos(angle)]
        ])
        return rot_matrix

    # <--- rotation --->
    def Rx(self, angle):
        rot = self.__rotInit__(angle)
        temp = np.eye(4, dtype=float)

        temp[1:3,1:3] = rot

        self.M = np.matmul(self.M, temp)
        return self

    def Ry(self, angle):
        rot = self.__rotInit__(angle)
        temp = np.eye(self.dim, dtype=float)
        temp[np.ix_([0,2],[0,2])] = rot.transpose()

        self.M = np.matmul(self.M, temp)
        return self

    def Rz(self, angle):
        rot = self.__rotInit__(angle)
        temp = np.eye(self.dim, dtype=float)

        temp[:2,:2] = rot

        self.M = np.matmul(self.M, temp)
        return self

    # translation
    def T(self, vector:list):
        temp = np.eye(self.dim, dtype=float)
        temp[:3, -1] = np.array(vector)

        self.M = np.matmul(self.M, temp)
        return self
