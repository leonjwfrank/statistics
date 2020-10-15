# py adapter case  结构化-适配器类实现
import itertools


class Ploygon(object):
    """A polygon class"""

    def __init__(self, *sides):
        """Initializer accepts length of sides"""
        self.sides = sides

    def perimeter(self):
        """Return perimeter"""
        return sum(self.sides)

    def is_valid(self):
        """Is this a valid polygon"""
        # Do som complex stuff not implemented in base class
        raise NotImplementedError

    def is_regular(self):
        """Is a regular polygon?"""
        # Yes, if all sides are equal
        side = self.sides[0]
        return all([x == side for x in self.sides[1:]])

    def area(self):
        """Calculate and return area"""
        # Not implemented in base class
        raise NotImplementedError


class InvalidPolygonError(Exception):
    pass


class Triangle(Ploygon):
    """Triangle（三角） class from Polygon（多边形） using class adapter（适配）"""

    def is_equilateral(self):
        """Is this an equilateral triangle? 等边三角？"""
        if self.is_valid():
            return super(Triangle, self).is_regular()

    def is_isosceles(self):
        """Is the triangle isosceles 等腰三角？"""
        if self.is_valid():
            # Check if any 2 sides are equal
            for a, b in itertools.combinations(self.sides, 2):
                if a == b:
                    return True
        return False

    def is_right(self):
        """根据毕达哥拉斯定理(勾股定理)判断，是否直角三角形 right triangle"""
        _sides = sorted(self.sides)
        if _sides[0] ** 2 + _sides[1] ** 2 == _sides[-1] ** 2:
            return True
        return False

    def area(self):
        """Calculate area  三角面积"""
        # Using Heron's formula
        p = self.perimeter() / 2.0
        total = p
        for side in self.sides:
            total *= abs(p - side)
        return pow(total, 0.5)

    def area_def(self):
        """三角面积，底*高 的一半"""
        # Using default method

    def is_valid(self):
        """Is the triangle valid 有效三角？"""
        # Sum of 2 sides should be > 3rd side
        perimeter = self.perimeter()
        for side in self.sides:
            sum_two = perimeter - side
            if sum_two <= side:
                raise InvalidPolygonError(str(self.__class__) + 'is invalid')
        return True


class Rectangle(Ploygon):
    """Rectangle class from Polygon using class adapter 长方形"""

    def is_square(self):
        """Return if I am a square 是否正方形"""
        if self.is_valid():
            # Defaults to is_regular
            return self.is_regular()   # 所有边是否相等

    def is_valid(self):
        """IS the rectangle valid"""
        # Should have 4 sides
        if len(self.sides) != 4:
            return False
        # Opposite sides should be same 判断相对的两条边是否一致
        for a, b in [(0, 2), (1, 3)]:
            if self.sides[a] != self.sides[b]:
                return False
        return True

    def area(self):
        """Return area of rectangle"""
        # Length x breadth
        if self.is_valid():
            return self.sides[0] * self.sides[1]


if __name__ == '__main__':
    pass
    t1 = Triangle(3,4,5)
    print(f'合法三角形?', t1.is_valid())
    print(f'等边三角?', t1.is_equilateral())
    print(f'等腰三角?', t1.is_isosceles())
    print(f'三角面积?', t1.area())
    print(f"直角三角形?", t1.is_right())

    t2 = Triangle(2, 2, 3)
    print(t2.is_equilateral())
    print(t2.is_isosceles())
    print(t2.area())

    r1 = Rectangle(2,2, 3, 3)
    print(f"r1矩形？{r1.is_valid()}")

    r2 = Rectangle(2,3,2,3)
    print(f"r2矩形? {r2.is_valid()}")
    print(f"r2矩形面积?{r2.area()}")

    r3 = Rectangle(5,5,5,5)
    print(f"r3是否正方形?{r3.is_square()}")