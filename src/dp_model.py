def compute_dp_table(S, T, ins_cost, del_cost, sub_cost):
    """
    Computes the DP table for DNA mutation pathway reconstruction.

    dp[i][j] = minimum cost to convert S[0:i] into T[0:j]
    """

    n, m = len(S), len(T)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    choice = [[None] * (m + 1) for _ in range(n + 1)]

    # Base cases
    for i in range(1, n + 1):
        dp[i][0] = i * del_cost
        choice[i][0] = "DELETE"

    for j in range(1, m + 1):
        dp[0][j] = j * ins_cost
        choice[0][j] = "INSERT"

    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if S[i - 1] == T[j - 1]:
                sub = dp[i - 1][j - 1]
                sub_action = "MATCH"
            else:
                sub = dp[i - 1][j - 1] + sub_cost
                sub_action = "SUBSTITUTE"

            delete = dp[i - 1][j] + del_cost
            insert = dp[i][j - 1] + ins_cost

            dp[i][j] = min(sub, delete, insert)

            if dp[i][j] == sub:
                choice[i][j] = sub_action
            elif dp[i][j] == delete:
                choice[i][j] = "DELETE"
            else:
                choice[i][j] = "INSERT"

    return dp, choice
