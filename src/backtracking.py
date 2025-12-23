def reconstruct_path(choice, S, T, verbose=True, visual_callback=None):
    """
    Reconstructs the mutation steps using backtracking
    and prints each step during traversal.
    """

    i, j = len(S), len(T)
    steps = []

    if verbose:
        print("\nBacktracking Steps:")

    while i > 0 or j > 0:
        action = choice[i][j]

        # Call the visual callback if provided
        if visual_callback is not None:
            visual_callback(i, j, action)

        if action == "MATCH":
            if verbose:
                print(f"At dp[{i}][{j}]: MATCH '{S[i-1]}' → move to dp[{i-1}][{j-1}]")
            i -= 1
            j -= 1

        elif action == "SUBSTITUTE":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: SUBSTITUTE '{S[i-1]}' → '{T[j-1]}' "
                    f"→ move to dp[{i-1}][{j-1}]"
                )
            steps.append(f"Substitute {S[i-1]} → {T[j-1]}")
            i -= 1
            j -= 1

        elif action == "DELETE":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: DELETE '{S[i-1]}' "
                    f"→ move to dp[{i-1}][{j}]"
                )
            steps.append(f"Delete {S[i-1]}")
            i -= 1

        elif action == "INSERT":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: INSERT '{T[j-1]}' "
                    f"→ move to dp[{i}][{j-1}]"
                )
            steps.append(f"Insert {T[j-1]}")
            j -= 1

        else:
            raise ValueError(f"Unknown action at dp[{i}][{j}]")

    return steps[::-1]
