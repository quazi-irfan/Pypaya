from Matrix import Matrix
import numpy

class Node:
    def __init__(self, name=None):
        self.name = name
        self.parent = None
        self.children = []
        self.modelMatrix = Matrix.identity()

    def __str__(self):
        return self.name

    def addChild(self, child):
        child.parent = self
        # New modelMatrix can be calculate analytically/ using closed form solution
        # https://stackoverflow.com/questions/27308525/how-to-compare-pose-and-position-of-two-objects-from-rotation-and-translation-ma
        child.modelMatrix = child.modelMatrix @ numpy.linalg.inv(self.modelMatrix)
        self.children.append(child)

    def getWorldMatrix(self):
        if self.parent:
            # Combine parent's modelMatrix with local modelMatrix; Meaning we are getting accumulated modelMatrix from the original
            return self.parent.getWorldMatrix() @ self.modelMatrix
        else:
            return self.modelMatrix

    def getPosition(self, local=True):
        if not local:
            worldTransform = self.getWorldMatrix()
            return [worldTransform.item((0, 3)), worldTransform.item((1, 3)), worldTransform.item((2, 3))]
        else:
            return [self.modelMatrix.item((0, 3)), self.modelMatrix.item((1, 3)), self.modelMatrix.item((2, 3))]

    def setGlobalPosition(self, x, y, z):
        self.modelMatrix.itemset((0, 3), x)
        self.modelMatrix.itemset((1, 3), y)
        self.modelMatrix.itemset((2, 3), z)

    def translate(self, x, y, z, local=True):
        self.modelMatrix = self.modelMatrix @ Matrix.translate(x, y, z)

    def rotate(self, axis, angle, local=True):
        if axis == 'x':
            rotationMatrix = Matrix.rotateX(angle)
        elif axis == 'y':
            rotationMatrix = Matrix.rotateY(angle)
        elif axis == 'z':
            rotationMatrix = Matrix.rotateZ(angle)

        self.modelMatrix = self.modelMatrix @ rotationMatrix


    def scale(self, factor, local=True):
        self.modelMatrix = self.modelMatrix @ Matrix.scale(factor)

class Camera(Node):
    def __init__(self, width, height):
        from math import sin, cos, tan, pi

        super().__init__()

        angleOfView = 60
        aspectRatio = width / height
        near = 0.1
        far = 100

        a = angleOfView * pi / 180.0
        d = 1.0 / tan(a / 2)
        r = aspectRatio
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)

        self.projectionMatrix = numpy.array([
            [d / r, 0, 0, 0],
            [0, d, 0, 0],
            [0, 0, b, c],
            [0, 0, -1, 0]]).astype(float)