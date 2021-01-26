"""Module containing pyvista implementation of vtkCamera."""
from typing import Sequence, Optional, List

import numpy as np
import vtk

from pyvista.typing import Vector, NumericArray


class Camera(vtk.vtkCamera):
    """Camera class."""

    def __init__(self):
        """Initialize a new camera descriptor."""
        self._position = self.GetPosition()
        self._focus = self.GetFocalPoint()
        self._is_parallel_projection = False

    @property
    def position(self) -> Vector:
        """Position of the camera in world coordinates."""
        return self._position

    @position.setter
    def position(self, value: Vector):
        self.SetPosition(value)
        self._position = self.GetPosition()

    @property
    def focal_point(self) -> Vector:
        """Location of the camera's focus in world coordinates."""
        return self._focus

    @focal_point.setter
    def focal_point(self, point: Vector):
        self.SetFocalPoint(point)
        self._focus = self.GetFocalPoint()

    @property
    def model_transform_matrix(self) -> np.ndarray:
        """Model transformation matrix."""
        vtk_matrix = self.GetModelTransformMatrix()
        matrix = np.empty((4, 4))
        vtk_matrix.DeepCopy(matrix.ravel(), vtk_matrix)
        return matrix

    @model_transform_matrix.setter
    def model_transform_matrix(self, matrix: np.ndarray):
        vtk_matrix = vtk.vtkMatrix4x4()
        vtk_matrix.DeepCopy(matrix.ravel())
        self.SetModelTransformMatrix(vtk_matrix)

    @property
    def is_parallel_projection(self) -> bool:
        """Return True if parallel projection is set."""
        return self._is_parallel_projection

    @property
    def distance(self) -> float:
        """Distance from the camera position to the focal point."""
        return self.GetDistance()

    @property
    def thickness(self) -> float:
        """Distance between clipping planes."""
        return self.GetThickness()

    @thickness.setter
    def thickness(self, length: float):
        self.SetThickness(length)

    @property
    def parallel_scale(self) -> float:
        """Scaling used for a parallel projection, i.e."""
        return self.GetParallelScale()

    @parallel_scale.setter
    def parallel_scale(self, scale: float):
        self.SetParallelScale(scale)

    def zoom(self, value: float):
        """Zoom of the camera."""
        self.Zoom(value)

    # TODO, type hints, correct return type?
    def up(self, vector: Optional[Vector]=None) -> Optional[Vector]:
        """Up of the camera."""
        if vector is None:
            return self.GetViewUp()
        else:
            self.SetViewUp(vector)

    def enable_parallel_projection(self, flag: Optional[bool]=True):
        """Enable parallel projection.

        The camera will have a parallel projection. Parallel projection is
        often useful when viewing images or 2D datasets.

        """
        self._is_parallel_projection = flag
        self.SetParallelProjection(flag)

    def disable_parallel_projection(self):
        """Reset the camera to use perspective projection."""
        self.enable_parallel_projection(False)

    @property
    def clipping_range(self) -> List[float]:
        """Clipping range."""
        return self.GetClippingRange()

    @clipping_range.setter
    def clipping_range(self, points: NumericArray):
        if points[0] > points[1]:
            raise ValueError(f'Near point should lower than far point.')
        self.SetClippingRange(points[0], points[1])

    def __del__(self):
        """Delete the camera."""
        self.RemoveAllObservers()
        self.parent = None
