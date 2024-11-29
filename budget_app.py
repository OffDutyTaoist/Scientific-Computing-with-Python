class Category:
    def __init__(self, name):
        """
        Initialize the Category class with a name and an empty ledger.
        """
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """
        Add a deposit to the ledger with the given amount and description.
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Add a withdrawal to the ledger as a negative amount if there are enough funds.
        Return True if the withdrawal was successful, False otherwise.
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """
        Calculate and return the current balance of the ledger.
        """
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, other_category):
        """
        Transfer the specified amount to another category.
        Return True if the transfer was successful, False otherwise.
        """
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {other_category.name}")
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """
        Check if there are enough funds to cover the specified amount.
        Return True if there are sufficient funds, False otherwise.
        """
        return self.get_balance() >= amount

    def __str__(self):
        """
        Return a string representation of the Category, including the ledger and balance.
        """
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            desc = entry["description"][:23]
            amount = f"{entry['amount']:.2f}"
            items += f"{desc:<23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    """
    Create a bar chart representing the percentage spent in each category.
    """
    # Calculate total spending and percentage spent per category
    total_spent = 0
    category_spent = []
    for category in categories:
        spent = sum(-entry["amount"] for entry in category.ledger if entry["amount"] < 0)
        total_spent += spent
        category_spent.append((category.name, spent))

    # Calculate percentages
    percentages = [(name, int((spent / total_spent) * 100) // 10 * 10) for name, spent in category_spent]

    # Build chart
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for _, percent in percentages:
            chart += "o  " if percent >= i else "   "
        chart += "\n"

    # Add horizontal line
    chart += "    -" + "---" * len(categories) + "\n"

    # Add category names
    max_length = max(len(name) for name, _ in percentages)
    names = [name.ljust(max_length) for name, _ in percentages]
    for i in range(max_length):
        chart += "     " + "  ".join(name[i] for name in names) + "  \n"

    return chart.rstrip("\n")


# Example usage
if __name__ == "__main__":
    food = Category("Food")
    food.deposit(1000, "initial deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food for dessert")

    clothing = Category("Clothing")
    food.transfer(50, clothing)
    clothing.withdraw(25.55)
    clothing.withdraw(100)

    auto = Category("Auto")
    auto.deposit(1000, "initial deposit")
    auto.withdraw(15)

    print(food)
    print(clothing)
    print(auto)
    print(create_spend_chart([food, clothing, auto]))
