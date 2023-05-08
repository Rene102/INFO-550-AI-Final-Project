def solve_n_queens_backtracking(n):
    board = [-1] * n

    def is_valid_move(row, col):
        for i in range(row):
            if (
                board[i] == col
                or board[i] - i == col - row
                or board[i] + i == col + row
            ):
                return False

        return True

    def backtrack(row):
        nonlocal board
        if row == n:
            return board[:]

        for col in range(n):
            if is_valid_move(row, col):
                board[row] = col

                result = backtrack(row + 1)

                if result is not None:
                    return result

        return None

    return backtrack(0)

print(solve_n_queens_backtracking(8))
