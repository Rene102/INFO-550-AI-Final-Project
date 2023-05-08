import time
from copy import deepcopy

def solve_n_queens_forward_checking(n):
    domains = {(i, j): set(range(n)) for i in range(n) for j in range(n)}

    def is_consistent():
        for (row1, col1), domain1 in domains.items():
            if len(domain1) == 1:
                for (row2, col2), domain2 in domains.items():
                    if (
                        (row1, col1) != (row2, col2)
                        and (row1 == row2 or col1 == col2 or row1 - col1 == row2 - col2)
                        and domain1.issubset(domain2)
                    ):
                        domain2.difference_update(domain1)

        return all(domain for (row, col), domain in domains.items() if table[row] == col)

    def backtrack(row):
        if row == n:
            return table

        for col in domains[(row, -1)]:
            table[row] = col

            new_domains = deepcopy(domains)

            for r in range(n):
                if (r, col) in new_domains:
                    new_domains[(r, col)] = {col}

                diff = row - r

                if (r + diff, col + diff) in new_domains:
                    new_domains[(r + diff, col + diff)].discard(col)

                if (r - diff, col + diff) in new_domains:
                    new_domains[(r - diff, col + diff)].discard(col)

            if is_consistent():
                result = backtrack(row + 1)

                if result is not None:
                    return result

            table[row] = -1

        return None

    table = [-1] * n
    start_time = time.time()
    solution = backtrack(0)
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")
    return solution
print(solve_n_queens_forward_checking(8))