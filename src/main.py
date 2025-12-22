from dp_model import compute_dp_table
from backtracking import reconstruct_path
from visualization import print_dp_table


def main():
    S = "ACGTAC"
    T = "AGTTC"

    ins_cost = 1
    del_cost = 1
    sub_cost = 2

    dp, choice = compute_dp_table(S, T, ins_cost, del_cost, sub_cost)
    steps = reconstruct_path(choice, S, T)

    print_dp_table(dp)
    print("\nMinimum Mutation Cost:", dp[len(S)][len(T)])

    print("\nMutation Steps:")
    for step in steps:
        print("-", step)


if __name__ == "__main__":
    main()
