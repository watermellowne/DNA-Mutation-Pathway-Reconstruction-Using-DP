import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dp_model import compute_dp_table

tests = [
    ("ACG", "ACG"),
    ("ACG", "AG"),
    ("AAA", "TTT"),
    ("", "ACG")
]

for S, T in tests:
    dp, _ = compute_dp_table(S, T, 1, 1, 2)
    print(f"{S} → {T} | Cost = {dp[len(S)][len(T)]}")
