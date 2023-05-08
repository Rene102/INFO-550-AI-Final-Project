import time

def solve_n_queens_constraint_propagation(n):
    def is_consistent(table, row, col):
        for i in range(row):
            if (
                table[i] == col
                or table[i] - i == col - row
                or table[i] + i == col + row
            ):
                return False

        return True

    def propagate_constraints(table, domains):
        for i in range(n):
            if table[i] != -1:
                for j in range(n):
                    if j != i:
                        if table[i] in domains[(j, i)]:
                            domains[(j, i)].remove(table[i])

                        diff = j - i

                        if table[i] + diff in domains[(j, i)]:
                            domains[(j, i)].remove(table[i] + diff)

                        if table[i] - diff in domains[(j, i)]:
                            domains[(j, i)].remove(table[i] - diff)

    def backtrack(table, row, domains):
        if row == n:
            return table

        for col in domains[(row, -1)]:
            if is_consistent(table, row, col):
                table[row] = col

                new_domains = domains.copy()

                propagate_constraints(table, new_domains)

                result = backtrack(table, row + 1, new_domains)

                if result is not None:
                    return result

                table[row] = -1

        return None

    table = [-1] * n
    domains = {(i, j): set(range(n)) for i in range(n) for j in range(n)}

    for i in range(n):
        for j in range(n):
            if i == j:
                domains[(i, j)] = {i}
            else:
                domains[(i, j)] = set(range(n))

    start_time = time.time()
    solution = backtrack(table, 0, domains)
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")

    return solution
print(solve_n_queens_constraint_propagation(8))
