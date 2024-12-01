class R2Vector:
    def __init__(self, *, x, y):
        """Initialize a 2D vector with x and y components."""
        self.x = x
        self.y = y

    def norm(self):
        """Calculate the Euclidean norm (magnitude) of the vector."""
        return sum(val**2 for val in vars(self).values())**0.5

    def __str__(self):
        """Provide a readable string representation of the vector."""
        return str(tuple(getattr(self, i) for i in vars(self)))

    def __repr__(self):
        """Provide a detailed string representation for debugging."""
        components = ', '.join(f'{key}={val}' for key, val in vars(self).items())
        return f"{self.__class__.__name__}({components})"

    def __add__(self, other):
        """Perform element-wise addition with another vector of the same class."""
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) + getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __sub__(self, other):
        """Perform element-wise subtraction with another vector of the same class."""
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) - getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __mul__(self, other):
        """Perform scalar multiplication or compute the dot product."""
        if type(other) in (int, float):
            # Scalar multiplication
            kwargs = {i: getattr(self, i) * other for i in vars(self)}
            return self.__class__(**kwargs)
        elif type(self) == type(other):
            # Dot product
            return sum(getattr(self, i) * getattr(other, i) for i in vars(self))
        return NotImplemented

    def __eq__(self, other):
        """Check if all components are equal."""
        if type(self) != type(other):
            return NotImplemented
        return all(getattr(self, i) == getattr(other, i) for i in vars(self))

    def __ne__(self, other):
        """Check if any component is not equal."""
        return not self == other

    def __lt__(self, other):
        """Compare vectors by their norms (less than)."""
        if type(self) != type(other):
            return NotImplemented
        return self.norm() < other.norm()

    def __gt__(self, other):
        """Compare vectors by their norms (greater than)."""
        if type(self) != type(other):
            return NotImplemented
        return self.norm() > other.norm()

    def __le__(self, other):
        """Compare vectors by their norms (less than or equal)."""
        return not self > other

    def __ge__(self, other):
        """Compare vectors by their norms (greater than or equal)."""
        return not self < other


class R3Vector(R2Vector):
    def __init__(self, *, x, y, z):
        """Initialize a 3D vector with x, y, and z components."""
        super().__init__(x=x, y=y)
        self.z = z

    def cross(self, other):
        """Compute the cross product of two 3D vectors."""
        if type(self) != type(other):
            return NotImplemented
        # Cross product formula for 3D vectors
        kwargs = {
            'x': self.y * other.z - self.z * other.y,
            'y': self.z * other.x - self.x * other.z,
            'z': self.x * other.y - self.y * other.x
        }
        return self.__class__(**kwargs)


# Test cases with functionality comments
v1 = R3Vector(x=2, y=3, z=1)  # Initialize a 3D vector
v2 = R3Vector(x=0.5, y=1.25, z=2)  # Initialize another 3D vector

print(f'v1 = {v1}')  # Display v1
print(f'v2 = {v2}')  # Display v2

# Test addition
v3 = v1 + v2
print(f'v1 + v2 = {v3}')  # Element-wise addition

# Test subtraction
v4 = v1 - v2
print(f'v1 - v2 = {v4}')  # Element-wise subtraction

# Test dot product
v5 = v1 * v2
print(f'v1 * v2 = {v5}')  # Dot product of v1 and v2

# Test cross product
v6 = v1.cross(v2)
print(f'v1 x v2 = {v6}')  # Cross product of v1 and v2
