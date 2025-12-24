from dp_model import compute_dp_table
from backtracking import reconstruct_path
from visualization import print_dp_table
import os

def read_dna_file(filename):
   


    # Reads a DNA sequence from a text file.
    sequence = ""
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines or FASTA headers
                if not line or line.startswith(">"):
                    continue
                # Append sequence line + Converts all characters to uppercase
                sequence += line.upper()
        return sequence
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

def main():
<<<<<<< HEAD
   
     # get the directory of file
=======

>>>>>>> 98f0ca00dabd45ea7cf0b1788eb8fc2026480edd
    script_dir = os.path.dirname(os.path.abspath(__file__))
   
    base_dir = os.path.dirname(script_dir)
<<<<<<< HEAD
    #file paths for sequences
    file_healthy = os.path.join(base_dir, "Sequences", "kras_healthy.txt")
    file_mutated = os.path.join(base_dir, "Sequences", "kras_mutated.txt")
=======
    file_healthy = os.path.join(base_dir, "Sequences", "Small_Example_healthy.txt")
    file_mutated = os.path.join(base_dir, "Sequences", "Small_Example_mutated.txt")
>>>>>>> 98f0ca00dabd45ea7cf0b1788eb8fc2026480edd
    print(f"Reading sequences from files...")

    # Read sequences from files
    healthy_DNA = read_dna_file(file_healthy)
    mutated_DNA = read_dna_file(file_mutated)

    # Check if files were read successfully
    if healthy_DNA is None or mutated_DNA is None:
        print("Aborting due to file error.")
        return

    # Check if files are empty
    if not healthy_DNA or not mutated_DNA:
        print("Error: One or both of the DNA files are empty.")
        return
<<<<<<< HEAD
    # Display sequence lengths
    print(f"Healthy Sequence Length: {len(S)}")
    print(f"Mutated Sequence Length: {len(T)}")
    # Define mutation costs
=======

    print(f"Healthy Sequence Length: {len(healthy_DNA)}")
    print(f"Mutated Sequence Length: {len(mutated_DNA)}")

>>>>>>> 98f0ca00dabd45ea7cf0b1788eb8fc2026480edd
    ins_cost = 2
    del_cost = 2
    sub_cost = 1

    
<<<<<<< HEAD
    dp, choice = compute_dp_table(S, T, ins_cost, del_cost, sub_cost)
    # Display DP table 
    print_dp_table(dp)  
    # Reconstruct mutation steps using backtracking
    steps = reconstruct_path(choice, S, T)

    
    
    # Display final mutation cost
    print("\nMinimum Mutation Cost:", dp[len(S)][len(T)])
=======
    dp, choice = compute_dp_table(mutated_DNA, healthy_DNA, ins_cost, del_cost, sub_cost)
    
    print_dp_table(dp)  

    steps = reconstruct_path(choice, mutated_DNA, healthy_DNA)

    # if len(S) < 20:
    #     print_dp_table(dp)
    # else:
    #     print("\n(DP Table is too large to display)")

    print("\nMinimum Mutation Cost:", dp[len(mutated_DNA)][len(healthy_DNA)])
>>>>>>> 98f0ca00dabd45ea7cf0b1788eb8fc2026480edd

    print("\nMutation Steps:")
    for step in steps:
        print("-", step)

    

if __name__ == "__main__":
    main()