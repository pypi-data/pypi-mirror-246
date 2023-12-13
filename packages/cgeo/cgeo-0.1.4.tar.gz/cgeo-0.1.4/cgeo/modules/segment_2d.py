from __future__ import annotations
from typing import Union
from cgeo.modules.point_2d import Point2D as Point
from cgeo.utilities.error_handling.error_utilities import *

from cgeo import _cgeo

@handle_errors_for_class
class Segment2D:
    def __init__(self, *args):
        if len(args) == 1:
            assert(isinstance(args[0], Segment2D) or isinstance(args[0], _cgeo.libShapes_2D.Segment))

            self._segment = _cgeo.libShapes_2D.Segment(args[0].origin.cPoint, args[0].target.cPoint) if isinstance(args[0], Segment2D) else args[0]
            self._origin = args[0].origin if (isinstance(args[0], Segment2D)) else Point.fromCPoint(args[0].origin)
            self._target = args[0].target if (isinstance(args[0], Segment2D)) else Point.fromCPoint(args[0].target)
        elif len(args) == 2:
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            self._segment = _cgeo.libShapes_2D.Segment(args[0].cPoint, args[1].cPoint)
            self._origin = args[0]
            self._target = args[1]
        else:
            raise ValueError('incompatible amount of arguments')

    def __eq__(self, other: Segment2D) -> bool:
        return self._segment == other.cSegment

    def __ne__(self, other: Segment2D) -> bool:
        return self._segment != other.cSegment

    def __copy__(self):
        return Segment2D(self.origin, self.target)

    def __str__(self):
        return str(self._segment)

    @property
    def origin(self) -> Point:
        return self._origin

    @origin.setter
    def origin(self, value: Point) -> None:
        self._origin = Point.fromCPoint(value) if isinstance(value, _cgeo.libShapes_2D.Point) else value
        self._segment.origin = value if isinstance(value, _cgeo.libShapes_2D.Point) else value.cPoint

    @property
    def target(self) -> Point:
        return self._target

    @target.setter
    def target(self, value: Point) -> None:
        self._target = Point.fromCPoint(value) if isinstance(value, _cgeo.libShapes_2D.Point) else value
        self._segment = value if isinstance(value, _cgeo.libShapes_2D.Point) else value.cPoint

    @property
    def slope(self) -> float:
        return self._segment.getSlope()

    @property
    def length(self) -> float:
        return self._segment.getLength()

    @property
    def cSegment(self) -> _cgeo.libShapes_2D.Segment:
        return self._segment

    @property
    def isValid(self) -> bool:
        return self._segment.origin != self._segment.target

    @classmethod
    def fromCSegment(cls, cSegment: _cgeo.libShapes_2D.Segment):
        newSegment = cls(cSegment)
        return newSegment

    def __originX(self) -> float:
        return self.origin.x

    def __originY(self) -> float:
        return self.origin.y

    def __targetX(self) -> float:
        return self.target.x

    def __targetY(self) -> float:
        return self.target.y

    def getUpperPoint(self) -> Point:
        cPoint = self._segment.getUpper()
        return self.origin if self.__originX() == cPoint.x and self.__originY() == cPoint.y else self.target

    def adder(self, offsetPoint: Point) -> None:
        self._segment.adder(offsetPoint.cPoint)

    def rotate(self, d: float) -> None:
        self._segment.rotate(d)

    def oriePred(self, other: Union[Point, Segment2D]) -> float:
        if not isinstance(other, (Point, Segment2D)):
            raise TypeError('Invalid argument type. Expected Point or Segment2D.')

        if isinstance(other, Point):
            return self._segment.oriePred(other.cPoint)

        return self._segment.oriePred(other.cSegment)

    def isParallel(self, other: Segment2D) -> bool:
        return self._segment.isParallel(other.cSegment)

    def isVertical(self, other: Segment2D) -> bool:
        return self._segment.isVertical(other.cSegment)

    def dist(self, other: Union[Point, Segment2D]) -> float:
        if not isinstance(other, (Point, Segment2D)):
            raise TypeError('Invalid argument type. Expected Point or Segment2D.')

        if isinstance(other, Point):
            return self._segment.dist(other.cPoint)

        return self._segment.dist(other.cSegment)

    def isIntersect(self, other: Segment2D) -> bool:
        return self._segment.isIntersect(other.cSegment)

    def getIntersection(self, other: Segment2D) -> Point:
        if not self.isIntersect(other):
            return None
        return Point.fromCPoint(self._segment.getIntersection(other.cSegment))

    def getXfromY(self, y: float) -> float:
        return self._segment.getXfromY(y)

    def getYfromX(self, x: float) -> float:
        return self._segment.getYfromX(x)

    def doesPointContain(self, point: Point) -> bool:
        return self._segment.doesPointContain(point.cPoint)