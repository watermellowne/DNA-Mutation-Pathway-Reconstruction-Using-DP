from dp_model import compute_dp_table
from backtracking import reconstruct_path
from visualization import print_dp_table
import os

def read_dna_file(filename):
   
    sequence = ""
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines or FASTA headers
                if not line or line.startswith(">"):
                    continue
                sequence += line.upper()
        return sequence
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

def main():
   

    script_dir = os.path.dirname(os.path.abspath(__file__))


   
    base_dir = os.path.dirname(script_dir)
    file_healthy = os.path.join(base_dir, "Sequences", "kras_healthy.txt")
    file_mutated = os.path.join(base_dir, "Sequences", "kras_mutated.txt")
    print(f"Reading sequences from files...")

    # Read sequences from files
    S = read_dna_file(file_healthy)
    T = read_dna_file(file_mutated)

    # Check if files were read successfully
    if S is None or T is None:
        print("Aborting due to file error.")
        return

    # Check if files are empty
    if not S or not T:
        print("Error: One or both of the DNA files are empty.")
        return

    print(f"Healthy Sequence Length: {len(S)}")
    print(f"Mutated Sequence Length: {len(T)}")

    ins_cost = 2
    del_cost = 2
    sub_cost = 1

    
    dp, choice = compute_dp_table(S, T, ins_cost, del_cost, sub_cost)
    
    print_dp_table(dp)  

    steps = reconstruct_path(choice, S, T)

    
    # if len(S) < 20:
    #     print_dp_table(dp)
    # else:
    #     print("\n(DP Table is too large to display)")

    print("\nMinimum Mutation Cost:", dp[len(S)][len(T)])

    print("\nMutation Steps:")
    for step in steps:
        print("-", step)

    

if __name__ == "__main__":
    main()