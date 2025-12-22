import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
from src.dp_model import compute_dp_table

S = "ACGT"
T = "AGTT"

sub_costs = [1, 2, 3, 4]
results = []

for cost in sub_costs:
    dp, _ = compute_dp_table(S, T, 1, 1, cost)
    results.append(dp[len(S)][len(T)])

plt.plot(sub_costs, results, marker='o')
plt.xlabel("Substitution Cost")
plt.ylabel("Minimum Mutation Cost")
plt.title("Effect of Substitution Cost on Mutation Path")
plt.grid(True)
plt.show()
