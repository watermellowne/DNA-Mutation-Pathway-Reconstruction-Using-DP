def reconstruct_path(choice, healthy_DNA, mutated_DNA, verbose=True, visual_callback=None):
    """
    Reconstructs the mutation steps using backtracking
    and prints each step during traversal.
    """

    i, j = len(healthy_DNA), len(mutated_DNA)
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
                print(f"At dp[{i}][{j}]: MATCH '{healthy_DNA[i-1]}' → move to dp[{i-1}][{j-1}]")
            i -= 1
            j -= 1

        elif action == "SUBSTITUTE":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: SUBSTITUTE '{healthy_DNA[i-1]}' → '{mutated_DNA[j-1]}' "
                    f"→ move to dp[{i-1}][{j-1}]"
                )
            steps.append(f"Substitute {healthy_DNA[i-1]} → {mutated_DNA[j-1]}")
            i -= 1
            j -= 1

        elif action == "DELETE":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: DELETE '{healthy_DNA[i-1]}' "
                    f"→ move to dp[{i-1}][{j}]"
                )
            steps.append(f"Delete {healthy_DNA[i-1]}")
            i -= 1

        elif action == "INSERT":
            if verbose:
                print(
                    f"At dp[{i}][{j}]: INSERT '{mutated_DNA[j-1]}' "
                    f"→ move to dp[{i}][{j-1}]"
                )
            steps.append(f"Insert {mutated_DNA[j-1]}")
            j -= 1

        else:
            raise ValueError(f"Unknown action at dp[{i}][{j}]")

    return steps[::-1]
