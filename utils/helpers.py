"""
Helper functions for input validation and display.
"""

import datetime
def input_int(prompt, min_val=None, max_val=None, default=None):
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            val = int(val)
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


def input_float(prompt, min_val=None, default=None):
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            val = float(val)
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")


def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("This field cannot be empty.")


def input_date(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            return None
        try:
            datetime.datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("Date must be YYYY-MM-DD")


def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)


def print_table(headers, rows):

    if not rows:
        print("No data.")
        return

    # Print the headings
    for header in headers:
        print(header, end=" | ")

    print()

    # Print a line
    print("-" * 50)

    # Print the data
    for row in rows:
        for item in row:
            print(item, end=" | ")

        print()