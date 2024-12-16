import copy
import random

class Hat:
    """
    Represents a hat containing balls of different colors.
    """

    def __init__(self, **balls):
        """
        Initialize the Hat with the given number of balls of each color.

        Args:
            **balls: Variable arguments specifying the number of balls for each color.
        """
        self.contents = []
        for color, count in balls.items():
            self.contents.extend([color] * count)

    def draw(self, num_balls):
        """
        Draw a specified number of balls from the hat randomly without replacement.

        Args:
            num_balls (int): The number of balls to draw.

        Returns:
            list: A list of strings representing the colors of the balls drawn.
        """
        if num_balls >= len(self.contents):
            drawn_balls = self.contents[:]
            self.contents = []
            return drawn_balls

        return [self.contents.pop(random.randint(0, len(self.contents) - 1)) for _ in range(num_balls)]

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    """
    Perform an experiment to estimate the probability of drawing a certain group of balls.

    Args:
        hat (Hat): A hat object containing balls.
        expected_balls (dict): The expected group of balls to attempt to draw.
        num_balls_drawn (int): The number of balls to draw out of the hat in each experiment.
        num_experiments (int): The number of experiments to perform.

    Returns:
        float: The probability of drawing the expected balls.
    """
    successful_experiments = 0

    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        balls_drawn = hat_copy.draw(num_balls_drawn)

        # Count the occurrences of each ball in the drawn balls
        balls_drawn_count = {}
        for ball in balls_drawn:
            balls_drawn_count[ball] = balls_drawn_count.get(ball, 0) + 1

        # Check if all expected balls are in the drawn balls
        success = all(balls_drawn_count.get(color, 0) >= count for color, count in expected_balls.items())

        if success:
            successful_experiments += 1

    return successful_experiments / num_experiments

# Example usage
hat = Hat(blue=5, red=4, green=2)
probability = experiment(
    hat=hat,
    expected_balls={'red': 1, 'green': 2},
    num_balls_drawn=4,
    num_experiments=2000
)
print(probability)
