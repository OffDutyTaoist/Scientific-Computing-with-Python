class Shape:
    """
    Base class for shapes. All shapes should implement get_area and get_perimeter.
    """
    def get_area(self):
        raise NotImplementedError("Subclasses must implement get_area")

    def get_perimeter(self):
        raise NotImplementedError("Subclasses must implement get_perimeter")


class Rectangle(Shape):
    """
    Represents a rectangle with width and height.
    Provides methods to calculate area, perimeter, and other rectangle-specific functionalities.
    """
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive numbers.")
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be a positive number.")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be a positive number.")
        self._height = value

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** 0.5

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture. Showing a truncated version.\n" + ("*" * 50 + "\n") * 50
        return ("*" * self.width + "\n") * self.height

    def get_amount_inside(self, shape):
        if not isinstance(shape, Rectangle):
            raise TypeError("The argument must be an instance of Rectangle or Square.")
        return (self.width // shape.width) * (self.height // shape.height)

    def __str__(self):
        return (f"Rectangle(width={self.width}, height={self.height}, "
                f"area={self.get_area()}, perimeter={self.get_perimeter()})")

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.get_area() < other.get_area()


class Square(Rectangle):
    """
    Represents a square, inheriting from Rectangle.
    Ensures width and height are always equal and provides square-specific methods.
    """
    def __init__(self, side):
        super().__init__(side, side)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value

    @property
    def side(self):
        return self.width

    @side.setter
    def side(self, value):
        self.width = self.height = value

    def __str__(self):
        return f"Square(side={self.side}, area={self.get_area()}, perimeter={self.get_perimeter()})"


# Example Usage
if __name__ == "__main__":
    rect = Rectangle(10, 5)
    print(rect.get_area())  # 50
    rect.set_height = 3
    print(rect.get_perimeter())  # 26
    print(rect)  # Rectangle(width=10, height=3, area=30, perimeter=26)
    print(rect.get_picture())  # Picture representation

    sq = Square(9)
    print(sq.get_area())  # 81
    sq.side = 4
    print(sq.get_diagonal())  # 5.656854249492381
    print(sq)  # Square(side=4, area=16, perimeter=16)
    print(sq.get_picture())  # Picture representation

    rect.set_height = 8
    rect.set_width = 16
    print(rect.get_amount_inside(sq))  # 8
