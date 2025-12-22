def reconstruct_path(choice, S, T):
    """
    Reconstructs the mutation steps using backtracking.
    """

    i, j = len(S), len(T)
    steps = []

    while i > 0 or j > 0:
        action = choice[i][j]

        if action == "MATCH":
            i -= 1
            j -= 1

        elif action == "SUBSTITUTE":
            steps.append(f"Substitute {S[i-1]} → {T[j-1]}")
            i -= 1
            j -= 1

        elif action == "DELETE":
            steps.append(f"Delete {S[i-1]}")
            i -= 1

        elif action == "INSERT":
            steps.append(f"Insert {T[j-1]}")
            j -= 1

    return steps[::-1]
