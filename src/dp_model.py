def compute_dp_table(healthy_DNA, mutated_DNA, ins_cost, del_cost, sub_cost): # dp[i][j] = minimum cost to convert S[0:i] into T[0:j]

# Inputs:
    # healthy_DNA: str, healthy DNA sequence
    # mutated_DNA: str, mutated DNA sequence
    # ins_cost = 2
    #del_cost = 2
    #sub_cost = 1

    n, m = len(healthy_DNA), len(mutated_DNA) # lengths of sequences

    dp = [[0] * (m + 1) for _ in range(n + 1)] # DP table Initialization
    choice = [[None] * (m + 1) for _ in range(n + 1)] # To reconstruct path later 

    # Base cases 
    for i in range(1, n + 1): 
        dp[i][0] = i * del_cost 
        choice[i][0] = "DELETE"

    for j in range(1, m + 1): 
        dp[0][j] = j * ins_cost 
        choice[0][j] = "INSERT"

    # Fill DP table
    for i in range(1, n + 1): # Iterate over healthy_DNA
        for j in range(1, m + 1): # Iterate over mutated_DNA
            if healthy_DNA[i - 1] == mutated_DNA[j - 1]:
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
