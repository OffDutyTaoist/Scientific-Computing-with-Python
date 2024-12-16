import math

# Constants
GRAVITATIONAL_ACCELERATION = 9.81  # Acceleration due to gravity in m/s^2
PROJECTILE = "∙"  # Symbol used for the projectile path
x_axis_tick = "T"  # Symbol used for the x-axis
y_axis_tick = "⊣"  # Symbol used for the y-axis

class Projectile:
    """
    A class representing a projectile in motion under the influence of gravity.

    Attributes:
        speed (float): Initial velocity of the projectile in m/s.
        height (float): Initial height of the projectile in meters.
        angle (float): Launch angle of the projectile in degrees.
    """

    __slots__ = ('__speed', '__height', '__angle')

    def __init__(self, speed, height, angle):
        if speed <= 0:
            raise ValueError("Speed must be greater than zero.")
        if height < 0:
            raise ValueError("Height cannot be negative.")
        if not (0 <= angle <= 90):
            raise ValueError("Angle must be between 0 and 90 degrees.")

        self.__speed = speed
        self.__height = height
        self.__angle = math.radians(angle)
        
    def __str__(self):
        return f'''
Projectile details:
speed: {self.speed} m/s
height: {self.height} m
angle: {self.angle}°
displacement: {round(self.__calculate_displacement(), 1)} m
'''

    def __calculate_displacement(self):
        """
        Calculate the horizontal displacement of the projectile.
        """
        cos_angle = math.cos(self.__angle)
        sin_angle = math.sin(self.__angle)
        velocity_vertical = self.__speed * sin_angle
        term_under_sqrt = velocity_vertical**2 + 2 * GRAVITATIONAL_ACCELERATION * self.__height
        return (self.__speed * cos_angle * 
                (velocity_vertical + math.sqrt(term_under_sqrt)) / GRAVITATIONAL_ACCELERATION)
        
    def __calculate_y_coordinate(self, x):
        """
        Calculate the vertical position (y-coordinate) for a given horizontal position (x).
        """
        height_component = self.__height
        angle_component = math.tan(self.__angle) * x
        acceleration_component = GRAVITATIONAL_ACCELERATION * x**2 / (
            2 * self.__speed**2 * math.cos(self.__angle)**2)
        return height_component + angle_component - acceleration_component
    
    def calculate_all_coordinates(self, step=1):
        """
        Calculate all coordinates (x, y) for the projectile motion with an optional step size.
        """
        max_distance = self.__calculate_displacement()
        x_values = [i * step for i in range(int(max_distance / step) + 1)]
        return [(x, self.__calculate_y_coordinate(x)) for x in x_values]

    @property
    def height(self):
        return self.__height

    @property
    def angle(self):
        return round(math.degrees(self.__angle))

    @property
    def speed(self):
        return self.__speed

    @height.setter
    def height(self, n):
        if n < 0:
            raise ValueError("Height cannot be negative.")
        self.__height = n

    @angle.setter
    def angle(self, n):
        if not (0 <= n <= 90):
            raise ValueError("Angle must be between 0 and 90 degrees.")
        self.__angle = math.radians(n)

    @speed.setter
    def speed(self, s):
        if s <= 0:
            raise ValueError("Speed must be greater than zero.")
        self.__speed = s
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.speed}, {self.height}, {self.angle})'

class Graph:
    """
    A class for rendering the graph and table representation of the projectile's trajectory.
    """

    __slots__ = ('__coordinates',)

    def __init__(self, coord):
        self.__coordinates = coord

    def __repr__(self):
        return f"Graph({self.__coordinates})"

    def create_coordinates_table(self):
        """
        Create a table of x and y coordinates for the projectile trajectory.
        """
        table = '\n  x      y\n'
        for x, y in self.__coordinates:
            table += f'{x:>5.2f}{y:>10.2f}\n'
        return table

    def create_trajectory(self):
        """
        Create a graphical representation of the projectile's trajectory.
        """
        rounded_coords = [(round(x), round(y)) for x, y in self.__coordinates]
        x_max = max(rounded_coords, key=lambda i: i[0])[0]
        y_max = max(rounded_coords, key=lambda j: j[1])[1]
        
        # Create matrix with (0, 0) at the bottom left
        matrix_list = [[' ' for _ in range(x_max + 1)] for _ in range(y_max + 1)]
        for x, y in rounded_coords:
            matrix_list[y_max - y][x] = PROJECTILE  # Adjust for bottom-left origin

        # Add y-axis ticks
        matrix_list = [y_axis_tick + row for row in [''.join(row) for row in matrix_list]]

        # Add x-axis ticks
        x_axis = ' ' + x_axis_tick * (x_max + 1)
        matrix_list.append(x_axis)

        return "\n" + "\n".join(matrix_list) + "\n"

def projectile_helper(speed, height, angle):
    """
    A utility function to create a projectile and display its details, coordinates, and trajectory.
    """
    # Create a projectile instance
    projectile = Projectile(speed, height, angle)
    print(projectile)

    # Calculate coordinates and create graph
    coordinates = projectile.calculate_all_coordinates()
    graph = Graph(coordinates)

    # Print coordinates table
    print(graph.create_coordinates_table())

    # Print graph trajectory
    print(graph.create_trajectory())

# Call the helper function with chosen values
projectile_helper(15, 5, 60)
