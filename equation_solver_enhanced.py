from abc import ABC, abstractmethod
import re

# Abstract Base Class for equations
class Equation(ABC):
    degree: int  # Degree of the equation
    type: str  # Type of the equation

    def __init__(self, *args):
        if (self.degree + 1) != len(args):
            raise TypeError(
                f"'Equation' object takes {self.degree + 1} positional arguments but {len(args)} were given"
            )
        if any(not isinstance(arg, (int, float)) for arg in args):
            raise TypeError("Coefficients must be of type 'int' or 'float'")
        if args[0] == 0:
            raise ValueError("Highest degree coefficient must be different from zero")
        self.coefficients = {(len(args) - n - 1): arg for n, arg in enumerate(args)}

    def __init_subclass__(cls):
        if not hasattr(cls, "degree"):
            raise AttributeError(
                f"Cannot create '{cls.__name__}' class: missing required attribute 'degree'"
            )
        if not hasattr(cls, "type"):
            raise AttributeError(
                f"Cannot create '{cls.__name__}' class: missing required attribute 'type'"
            )

    def __str__(self):
        """String representation of the equation."""
        terms = [
            f"{coefficient:+}x**{n}" if n > 1 else
            f"{coefficient:+}x" if n == 1 else
            f"{coefficient:+}"
            for n, coefficient in sorted(self.coefficients.items(), reverse=True) if coefficient
        ]
        return ' '.join(terms).replace('x**1', 'x').replace('+x', 'x') + ' = 0'

    @abstractmethod
    def solve(self):
        """Abstract method to solve the equation."""
        pass

    @abstractmethod
    def analyze(self):
        """Abstract method to analyze the equation."""
        pass

# Linear Equation Class
class LinearEquation(Equation):
    degree = 1
    type = 'Linear Equation'

    def solve(self):
        a, b = self.coefficients.values()
        x = -b / a
        return [x]

    def analyze(self):
        slope, intercept = self.coefficients.values()
        return {'slope': slope, 'intercept': intercept}

# Quadratic Equation Class
class QuadraticEquation(Equation):
    degree = 2
    type = 'Quadratic Equation'

    def __init__(self, *args):
        super().__init__(*args)
        a, b, c = self.coefficients.values()
        self.delta = b**2 - 4 * a * c

    def solve(self):
        if self.delta < 0:
            return []
        a, b, _ = self.coefficients.values()
        x1 = (-b + (self.delta) ** 0.5) / (2 * a)
        x2 = (-b - (self.delta) ** 0.5) / (2 * a)
        if self.delta == 0:
            return [x1]
        return [x1, x2]

    def analyze(self):
        a, b, c = self.coefficients.values()
        x = -b / (2 * a)
        y = a * x**2 + b * x + c
        if a > 0:
            concavity = 'upwards'
            min_max = 'min'
        else:
            concavity = 'downwards'
            min_max = 'max'
        return {'x': x, 'y': y, 'min_max': min_max, 'concavity': concavity}

# Helper Functions for Formatting

def format_solution(results):
    """Format the solution section."""
    if not results:
        return ['No real roots']
    if len(results) == 1:
        return [f'x = {results[0]:+.3f}']
    return [f'x1 = {results[0]:+.3f}', f'x2 = {results[1]:+.3f}']

def format_details(details):
    """Format the details section based on the type of details."""
    if 'slope' in details:
        return [
            f'slope = {details["slope"]:>16.3f}',
            f'y-intercept = {details["intercept"]:>16.3f}'
        ]
    coord = f'({details["x"]:.3f}, {details["y"]:.3f})'
    return [
        f'concavity = {details["concavity"]:>12}',
        f'{details["min_max"]} = {coord:>18}'
    ]

def solver(equation: Equation) -> str:
    """Solve and analyze an equation, returning a formatted string."""
    if not isinstance(equation, Equation):
        raise TypeError("Argument must be an Equation object")

    # Header
    output_string = f'\n{equation.type:-^24}'
    output_string += f'\n\n{equation!s:^24}\n\n'

    # Solutions Section
    output_string += f'{"Solutions":-^24}\n\n'
    results = equation.solve()
    result_list = format_solution(results)
    output_string += '\n'.join(f'{result:^24}' for result in result_list) + '\n'

    # Details Section
    output_string += f'\n{"Details":-^24}\n\n'
    details = equation.analyze()
    details_list = format_details(details)
    output_string += '\n'.join(details_list) + '\n'

    # Summary Section
    output_string += f'\n{"Summary":-^24}\n\n'
    output_string += f'Number of Solutions: {len(results):>16}\n'
    if isinstance(equation, QuadraticEquation):
        output_string += f'Discriminant (Delta): {equation.delta:>16.3f}\n'

    return output_string

# Example Usage
lin_eq = LinearEquation(2, 3)
quadr_eq = QuadraticEquation(1, -3, 2)

print(solver(lin_eq))
print(solver(quadr_eq))
