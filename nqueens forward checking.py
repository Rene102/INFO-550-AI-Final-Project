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

        return all(domain for (row, col), domain in domains.items() if board[row] == col)

    def backtrack(row):
        nonlocal domains
        if row == n:
            return board[:]

        for col in domains[(row, -1)].copy():
            board[row] = col

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

            board[row] = -1
            domains = new_domains

        return None

    board = [-1] * n
    return backtrack(0)
print( solve_n_queens_forward_checking(4))