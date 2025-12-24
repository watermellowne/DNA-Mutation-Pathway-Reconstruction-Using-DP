def compute_dp_table(mutated_DNA, healthy_DNA, ins_cost, del_cost, sub_cost): 
    # dp[i][j] = minimum cost to convert mutated_DNA[0:i] into healthy_DNA[0:j]

# Inputs:
    # healthy_DNA: str, healthy DNA sequence
    # mutated_DNA: str, mutated DNA sequence
    # ins_cost = 2
    # del_cost = 2
    # sub_cost = 1

    n, m = len(mutated_DNA), len(healthy_DNA) # lengths of sequences

    dp = [[0 for j in range(m + 1)] for i in range(n + 1)] # DP table Initialization
    choice = [[None for j in range(m + 1)] for i in range(n + 1)] # To reconstruct path later 

    # Base cases 
    for i in range(1, n + 1):  # Initializing first column (delete all mutated bases)
        dp[i][0] = i * del_cost 
        choice[i][0] = "DELETE"

    for j in range(1, m + 1): # Initializing first row (insert healthy bases)
        dp[0][j] = j * ins_cost 
        choice[0][j] = "INSERT"

    # Fill DP table
    for i in range(1, n + 1): # Iterate over mutated_DNA # Fill Rows of DP table
        for j in range(1, m + 1): # Iterate over healthy_DNA # Fill Columns of DP table
            if mutated_DNA[i - 1] == healthy_DNA[j - 1]:
                sub = dp[i - 1][j - 1] # match = diagonal cost
                sub_action = "MATCH" 
            else:
                sub = dp[i - 1][j - 1] + sub_cost # diagonal cell cost + substitution cost
                sub_action = "SUBSTITUTE"

            # Get both Costs for delete and insert
            delete = dp[i - 1][j] + del_cost # upper cell cost + deletion cost
            insert = dp[i][j - 1] + ins_cost # left cell cost + insertion cost

            dp[i][j] = min(sub, delete, insert) # Choose minimum cost between the three operations

            if dp[i][j] == sub: # Match or Substitute
                choice[i][j] = sub_action
            elif dp[i][j] == delete: # Delete
                choice[i][j] = "DELETE"
            else: # Insert
                choice[i][j] = "INSERT"

    return dp, choice
