import math, pymunk
from d6_objects import *

def getNormal(shape):
    normals = []
    vertices = shape.get_vertices()
    n = len(vertices)

    for i in range(0,n):
        v1 = vertices[i]

        v2 = vertices[(i+1) % n]

        edgeX = v2[0] - v1[0]
        edgeY = v2[1] - v1[1]

    
        normal = (-edgeY, edgeX)        # using the principle of rotating by pi in unit circle
        normals.append(normal)

    return normals

def project(shape, axis):
    projection = []
    vertices = shape.get_vertices()
    for i in vertices:
        proj = i[0]*axis[0] + i[1]*axis[1]
        projection.append(proj)
    
    return (min(projection), max(projection))

def overlap(intv1, intv2):
    min1, max1 = intv1
    min2, max2 = intv2

    if max1 < min2 or max2 < min1:
        return False
    else:
        return True


def SATheorem(shape1, shape2):
    normals1 = getNormal(shape1)
    normals2 = getNormal(shape2)

    axes = normals1 + normals2

    for axis in axes:
        proj1 = project(shape1, axis)
        proj2 = project(shape2, axis)

        if not overlap(proj1, proj2):
            return False
    
    return True

# ===================================================

