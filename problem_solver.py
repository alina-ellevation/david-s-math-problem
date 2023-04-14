import sys
from random import randint, uniform


def main():
    ProblemSolver().lets_boogie(
        # Before running this script, change these values to your liking
        # or comment out the line(s) to use the default().
        # See DocStrings further below for more context.
        random_int_ceiling=100,
        no_of_runs=1000,
    )


class ProblemSolver:
    def __init__(self):
        self.successful_run_count = 0
        self.failed_run_count_zero_division = 0
        self.failed_run_count_other = 0

    def lets_boogie(self, random_int_ceiling=sys.maxsize, no_of_runs=1000):
        """
        :param random_int_ceiling:
          Highest allowed int for cells b11 and b13. Must be positive.
          Default is the max that your operating system allows,
          but you could set it to, let's say, 100 for b11 and b13 to be between 0-100.

        :param no_of_runs:
          To ensure ProblemSolver didn't just get a "lucky" combo of b11 and b13
          that it can handle, let's run it *this* many times -
          each time with new random ints for b11 and b13. Default is 1000 runs.
          NOTE - must be a positive int; to avoid repeated b11 & b13 combos across runs,
          this should also be LOWER THAN THE SQUARE OF random_int_ceiling.

        IMPORTANT: I'm purposely NOT allowing *negative* ints for b11 and b13 for now -
        I'd have to change my algorithm to support those. Not there yet.
        """
        self.successful_run_count = 0  # Start with fresh counts
        self.failed_run_count_zero_division = 0
        self.failed_run_count_other = 0

        for i in range(0, no_of_runs):
            self.run(i + 1, random_int_ceiling)
        print(
            f"\nSUCCESSFUL RUNS: {self.successful_run_count}"
            f"\nFAILED RUNS (ZERO DIVISION): {self.failed_run_count_zero_division}"
            f"\nFAILED RUNS (OTHER): {self.failed_run_count_other}"
        )

    def run(self, no_of_run, random_int_ceiling):
        """
        Complete one test run = calculate a valid d11 for *one* combo of b11 and b13.
        """
        b11 = randint(0, random_int_ceiling)
        b13 = randint(0, random_int_ceiling)
        print(f"\nTest Run #{no_of_run}: b11 = {b11}, b13 = {b13}")
        self.narrow_down_d11_until_valid(
            # Let's start with a random float for d11 - it really doesn't matter
            # as it'll get narrowed down anyway. This one can even be negative.
            d11_lower_limit=-sys.maxsize,
            d11_upper_limit=sys.maxsize,
            b11=b11,
            b13=b13,
        )

    def narrow_down_d11_until_valid(self, d11_lower_limit, d11_upper_limit, b11, b13):
        # Set d11 to a random float within the given range.
        d11 = uniform(d11_lower_limit, d11_upper_limit)

        # Calculate Excel cell values.
        d13 = 1 - d11
        f11 = (b11 * d11) - d13
        f13 = (b13 * d13) - d11

        try:
            # Check if f11 and f13 are within 1 percent of each other.
            percent_difference = abs((f11 - f13) / ((f11 + f13) / 2)) * 100
            if not percent_difference <= 1:
                # If not, narrow down the range for d11 based on which cell was larger:
                if f11 >= f13:  # decrease upper limit (to try a smaller d11 next)
                    d11_upper_limit = d11
                else:  # or, increase lower limit (to try a larger d11 next).
                    d11_lower_limit = d11
                # Now, do the whole thing again with the smaller range...
                self.narrow_down_d11_until_valid(
                    d11_lower_limit, d11_upper_limit, b11, b13
                )
            # ...until the condition is met.
            else:
                print(
                    f"Valid value found! d11 = {d11} "
                    f"---> f11 = {f11}, f13 = {f13}, % difference: {percent_difference}"
                )
                self.successful_run_count += 1
        # If f11 or f13 happen to be 0, you can't calculate a percentage difference
        # between them (since that would require dividing by 0).
        # This is not a "real failure" but rather stems from an "unlucky" combo
        # of b11, b13 and d11. Let's move on but count how often that happens.
        except ZeroDivisionError:
            print(f"OOPS! Can't calculate percentage against 0.")
            self.failed_run_count_zero_division += 1
        # Everything else should be considered an actual failure, let's count those too.
        except Exception as e:
            print(f"OOPS! Something else went wrong: {e}")
            self.failed_run_count_other += 1


if __name__ == "__main__":
    main()
