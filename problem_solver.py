import pandas as pd
from random import uniform


def main():
    for i in range(0, 1000):
        calculate()


def calculate(
    start_val_1=round(uniform(0, 40), 2),
    start_val_2=round(uniform(0, 40), 2),
    piece_of_1_lower_limit=0,
    piece_of_1_upper_limit=1,
):
    # Set piece_of_1 to a random float within 0 and 1 with up to 2 decimals
    piece_of_1 = uniform(piece_of_1_lower_limit, piece_of_1_upper_limit)

    # Calculate Excel cell values.
    other_piece_of_1 = 1 - piece_of_1
    result_1 = (start_val_1 * piece_of_1) - other_piece_of_1
    result_2 = (start_val_2 * other_piece_of_1) - piece_of_1

    try:
        # Check if result_val_1 and result_val_2 are within 1 percent of each other.
        percent_diff = abs((result_1 - result_2) / ((result_1 + result_2) / 2)) * 100
        if not percent_diff <= 1:
            # If not, narrow down the range for piece_of_1 based on which result_val was larger:
            if result_1 >= result_2:  # decrease upper limit (to try a smaller piece_of_1 next)
                piece_of_1_upper_limit = piece_of_1
            else:  # or, increase lower limit (to try a larger piece_of_1 next).
                piece_of_1_lower_limit = piece_of_1
            # Now, do the whole thing again with the smaller range...
            calculate(
                start_val_1, start_val_2, piece_of_1_lower_limit, piece_of_1_upper_limit
            )
        # ...until the condition is met.
        else:
            columns = ["Starting Values", "Piece of 1", "Result"]
            data = [
                [start_val_1, piece_of_1, result_1],
                [start_val_2, other_piece_of_1, result_2]
            ]
            df = pd.DataFrame(data, columns=columns, index=['#1', '#2'])
            print(df)

    except ZeroDivisionError:
        # If result_val_1 or result_val_2 happen to be 0,
        # you can't calculate a percentage difference between them.
        # This stems from an "unlucky" combo of start_val_1, start_val_2 and piece_of_1,
        # so let's just try again (which will start with a new piece_of_1).
        calculate(start_val_1, start_val_2)
    except Exception as e:
        # Everything else should be considered an actual failure.
        print(f"OOPS! Something else went wrong: {e}")


if __name__ == "__main__":
    main()
