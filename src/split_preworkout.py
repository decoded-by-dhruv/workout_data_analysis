import pandas as pd

def split_pre_workout(info):
    """
    Parse a string of pre-workout food items and return quantities of specific items.

    Args:
        info (str): A string containing food items separated by '&'. Each item may include
        a quantity and name (e.g., "2 banana") or just a name (e.g., "banana").
        Example: "2 banana & 1 apple & coffee".

    Returns:
        pd.Series: A pandas Series with quantities for banana_qty, apple_qty,
        coffee_qty, and sandwich_qty. Non-matching items are ignored.

    Notes:
        - If the input is not a string, returns a Series with all quantities set to 0.
        - Assumes a quantity of 1 if no quantity is specified for an item.
        - Item names are case-insensitive and stripped of extra whitespace.
    """

    # Initialize quantities for tracked food items
    banana_qty = apple_qty = coffee_qty = sandwich_qty = 0

    # Return zero quantities if input is not a string
    if not isinstance(info, str):
        return pd.Series({
            'banana_qty': 0,
            'apple_qty': 0,
            'coffee_qty': 0,
            'sandwich_qty': 0
        })

    # Split input string by '&' and strip whitespace from each item
    food_items = [i.strip() for i in info.split('&')]

    # Parse each item into quantity and name
    splitted = []
    for item in food_items:
        parts = item.split(' ', 1)
        if len(parts) == 2:
            qty, name = parts
            qty = int(qty)
        elif len(parts) == 1:
            name = parts[0]
            qty = 1
        else:
            qty, name = 0, ''

        splitted.append((qty, name.lower().strip()))

    # Aggregate quantities for specific food items
    for qty, name in splitted:
        if name == 'banana':
            banana_qty += qty
        elif name == 'apple':
            apple_qty += qty
        elif name == 'coffee':
            coffee_qty += qty
        elif name == 'sandwich':
            sandwich_qty += qty

    # Return quantities as a pandas Series
    return pd.Series({
        'banana_qty': banana_qty,
        'apple_qty': apple_qty,
        'coffee_qty': coffee_qty,
        'sandwich_qty': sandwich_qty
    })
