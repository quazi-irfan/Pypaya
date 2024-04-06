import numpy
from OpenGL.GL import *


class Geometry:
    # subclass, add data with attribute name, this attribute name will be used to get buffer reference
    def __init__(self):
        self.attributes = {}

    def addAttribute(self, data, binding):
        data = numpy.array(data).astype(numpy.float32)
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer) # Activate the vboRef
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW) # Upload vertex data to the video device
        # But we still don't know how to parse the data, which is why we have to use glVertexAttribPointer

        self.attributes[binding] = {'ref': buffer, 'type': GL_FLOAT, 'length': len(data), 'offset': 0}


class TriangleGeomery(Geometry):
    def __init__(self):
        super().__init__()

        self.addAttribute([[.0, .2, 0], [.2, -.2, .0], [-.2, -.2, 0.0]], 'vertex_position')
        self.addAttribute([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], 'vertex_color')
        # temp = random.random()
        # self.addAttribute([[temp] * 3, [temp] * 3, [temp] * 3], 'vertex_color')


class RectangularGeometry(Geometry):
    def __init__(self, width, height):
        super().__init__()

        P0 = [-width / 2, -height / 2, 0]
        P1 = [width / 2, -height / 2, 0]
        P2 = [-width / 2, height / 2, 0]
        P3 = [width / 2, height / 2, 0]
        C0, C1, C2, C3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        positionData = [P0, P1, P3, P0, P3, P2]
        colorData = [C0, C1, C3, C0, C3, C2]

        self.addAttribute(positionData, 'vertex_position')
        self.addAttribute(colorData, 'vertex_color')


class BoxGeometry(Geometry):
    def __init__(self, width, height, depth):
        super().__init__()

        P0 = [-width / 2, -height / 2, -depth / 2]
        P1 = [width / 2, -height / 2, -depth / 2]
        P2 = [-width / 2, height / 2, -depth / 2]
        P3 = [width / 2, height / 2, -depth / 2]
        P4 = [-width / 2, -height / 2, depth / 2]
        P5 = [width / 2, -height / 2, depth / 2]
        P6 = [-width / 2, height / 2, depth / 2]
        P7 = [width / 2, height / 2, depth / 2]

        C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
        C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
        C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]

        positionData = [P5, P1, P3, P5, P3, P7, P0, P4, P6, P0, P6, P2, P6, P7, P3, P6, P3, P2, P0, P1, P5, P0, P5, P4,
                        P4, P5, P7, P4, P7, P6, P1, P0, P2, P1, P2, P3]

        colorData = [C1] * 6 + [C2] * 6 + [C3] * 6 + [C4] * 6 + [C5] * 6 + [C6] * 6 # Each face has 6 vertices. All vertices of a face gets the same vertex color

        self.addAttribute(positionData, 'vertex_position')
        self.addAttribute(colorData, 'vertex_color')


class PolygonGeometry(Geometry):
    def __init__(self, sides=3, radius=1):
        super().__init__()

        A = 2 * pi / sides
        positionData = []
        colorData = []

        for n in range(sides):
            positionData.append([0, 0, 0])
            positionData.append([radius * cos(n * A), radius * sin(n * A), 0])
            positionData.append([radius * cos((n + 1) * A), radius * sin((n + 1) * A), 0])
            colorData.append([1, 1, 1])
            colorData.append([1, 0, 0])
            colorData.append([0, 0, 1])

        self.addAttribute(positionData, 'vertex_position')
        self.addAttribute(colorData, 'vertex_color')


class ParametricGeometry(Geometry):
    def __init__(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
        super().__init__()
        # generate set of points on function
        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / vResolution
        positions = []

        for uIndex in range(uResolution + 1):
            vArray = []
            for vIndex in range(vResolution + 1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append(surfaceFunction(u, v))
            positions.append(vArray)

            # store vertex data
            self.positionData = []
            self.colorData = []

            # default vertex colors
            C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
            C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

            for xIndex in range(uResolution):
                for yIndex in range(vResolution):
                    pA = positions[xIndex + 0][yIndex + 0]
                    pB = positions[xIndex + 1][yIndex + 0]
                    pD = positions[xIndex + 0][yIndex + 1]
                    pC = positions[xIndex + 1][yIndex + 1]
                    self.positionData += [pA.copy(), pB.copy(), pC.copy(), pA.copy(), pC.copy(), pD.copy()]
                    self.colorData += [C1, C2, C3, C4, C5, C6]


class PlaneGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, widthSegments=8, heightSegments=8):
        def S(u, v):
            return [u, v, 0]

        super().__init__(-width / 2, width / 2, widthSegments, -height / 2, height / 2, heightSegments, S)

        self.addAttribute(self.positionData, 'vertex_position')
        self.addAttribute(self.colorData, 'vertex_color')