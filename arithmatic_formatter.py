def arithmetic_arranger(problems, show_answers=False):
    # Error check for too many problems
    if len(problems) > 5:
        return 'Error: Too many problems.'

    # Initialize lists to hold each line of the arranged problems
    first_operands = []
    operators = []
    second_operands = []
    lines = []
    answers = []

    # Loop through each problem to validate and format
    for problem in problems:
        parts = problem.split()

        # Check if there are exactly three parts (operand operator operand)
        if len(parts) != 3:
            return "Error: Incorrect problem format."

        first, operator, second = parts

        # Check for valid operators
        if operator not in ['+', '-']:
            return "Error: Operator must be '+' or '-'."

        # Check that operands contain only digits
        if not (first.isdigit() and second.isdigit()):
            return 'Error: Numbers must only contain digits.'

        # Check operand length
        if len(first) > 4 or len(second) > 4:
            return 'Error: Numbers cannot be more than four digits.'

        # Calculate answer if needed
        if show_answers:
            if operator == '+':
                answer = str(int(first) + int(second))
            else:
                answer = str(int(first) - int(second))
            answers.append(answer)

        # Calculate width for each problem (align based on longest operand)
        width = max(len(first), len(second)) + 2
        first_operands.append(first.rjust(width))
        operators.append(operator + ' ' + second.rjust(width - 2))
        lines.append('-' * width)

    # Combine each row with four spaces between problems
    arranged_problems = '    '.join(first_operands) + '\n'
    arranged_problems += '    '.join(operators) + '\n'
    arranged_problems += '    '.join(lines)

    # Add answers if show_answers is True
    if show_answers:
        arranged_problems += '\n' + '    '.join(answer.rjust(len(line)) for answer, line in zip(answers, lines))

    return arranged_problems

# Test cases
print(arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]))
print()
print(arithmetic_arranger(["3 + 855", "988 + 40"], True))
