import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextBrowser  # Better for formatted text

from dp_model import compute_dp_table
from backtracking import reconstruct_path

from visualization import print_dp_table


class DNAMutationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNA Mutation Pathway Reconstruction (DP)")
        self.setGeometry(300, 200, 600, 450)
        self.setup_ui()

    def setup_ui(self):
        self.label_s = QLabel("Mutated DNA File (Sequence 1):")
        self.s_path = QLineEdit()
        self.s_path.setReadOnly(True)
        self.s_btn = QPushButton("Browse")
        self.s_btn.clicked.connect(self.load_initial_file)

        self.label_t = QLabel("Healthy DNA File (Sequence 2):")
        self.t_path = QLineEdit()
        self.t_path.setReadOnly(True)
        self.t_btn = QPushButton("Browse")
        self.t_btn.clicked.connect(self.load_target_file)

        self.run_btn = QPushButton("Run Dynamic Programming")
        self.run_btn.clicked.connect(self.run_dp)

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Tab 1: Results
        self.results_tab = QWidget()
        results_layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        results_layout.addWidget(self.output)
        self.results_tab.setLayout(results_layout)
        
        # Tab 2: Backtracking
        self.backtracking_tab = QWidget()
        backtracking_layout = QVBoxLayout()
        self.backtracking_output = QTextEdit()
        self.backtracking_output.setReadOnly(True)
        backtracking_layout.addWidget(self.backtracking_output)
        self.backtracking_tab.setLayout(backtracking_layout)
        
        # Tab 3: DP Table
        self.dp_table_tab = QWidget()
        dp_table_layout = QVBoxLayout()
        self.dp_table_widget = QTableWidget()
        self.dp_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dp_table_widget.setAlternatingRowColors(True)
        dp_table_layout.addWidget(self.dp_table_widget)
        self.dp_table_tab.setLayout(dp_table_layout)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.results_tab, "Results")
        self.tab_widget.addTab(self.backtracking_tab, "Backtracking Steps")
        self.tab_widget.addTab(self.dp_table_tab, "DP Table")
        
        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_s)
        layout.addWidget(self.s_path)
        layout.addWidget(self.s_btn)
        layout.addWidget(self.label_t)
        layout.addWidget(self.t_path)
        layout.addWidget(self.t_btn)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.tab_widget)  # Add tab widget instead of individual text edits
        
        self.setLayout(layout)
        self.resize(800, 600)  # Make window larger to accommodate table

    def run_dp(self):

        # Clear outputs
        self.output.clear()
        self.backtracking_output.clear()
        
        if not self.s_path.text() or not self.t_path.text():
            QMessageBox.warning(self, "Error", "Please select both DNA files.")
            return
        
        # Read sequences
        S = self.read_dna_from_file(self.s_path.text())
        T = self.read_dna_from_file(self.t_path.text())
        
        if not S or not T:
            QMessageBox.warning(self, "Error", "Could not read valid DNA sequences from files.")
            return
        
        # Display sequence info first
        self.output.append("=" * 60)
        self.output.append("DNA MUTATION PATHWAY ANALYSIS")
        self.output.append("=" * 60)
        self.output.append(f"Mutated DNA length: {len(S)} bp")
        self.output.append(f"Healthy DNA length: {len(T)} bp")
        
        # Validate
        if not self.valid_dna(S):
            invalid_chars = ''.join(sorted(set(c for c in S if c not in "ACGT")))
            QMessageBox.warning(self, "Error", 
                f"Mutated DNA contains invalid characters: {invalid_chars[:50]}")
            return
        
        if not self.valid_dna(T):
            invalid_chars = ''.join(sorted(set(c for c in T if c not in "ACGT")))
            QMessageBox.warning(self, "Error", 
                f"Healthy DNA contains invalid characters: {invalid_chars[:50]}")
            return
        
        # Show preview of sequences (not full 2619 bp)
        self.output.append("\nSEQUENCE PREVIEW (first 100 bp):")
        self.output.append(f"Mutated: {S[:100]}...")
        self.output.append(f"Healthy: {T[:100]}...")
        
        # Run DP
        dp, choice = compute_dp_table(S, T, 2, 2, 1)

        self.display_dp_table_text(dp, S, T)


        if len(S) <= 40 and len(T) <= 40:  # Adjust threshold as needed
            self.display_dp_table(dp, S, T)
        else:
            self.display_dp_table_preview(dp, S, T, max_size=15)

        
        # Results
        self.output.append(f"\nMinimum Edit Distance: {dp[len(S)][len(T)]}")
        self.output.append("\nMUTATION PATHWAY:")
        
        steps = reconstruct_path(choice, T, S, verbose=False, visual_callback=self.visualize_step)
        
        # Count mutation types
        sub_count = sum(1 for step in steps if "Substitute" in step)
        ins_count = sum(1 for step in steps if "Insert" in step)
        del_count = sum(1 for step in steps if "Delete" in step)
        
        self.output.append(f"\nSummary: {len(steps)} total operations")
        self.output.append(f"  Substitutions: {sub_count}")
        self.output.append(f"  Insertions: {ins_count}")
        self.output.append(f"  Deletions: {del_count}")
        
        # Show first few steps if many
        if len(steps) > 20:
            self.output.append("\nFirst 20 steps:")
            for i, step in enumerate(steps[:20], 1):
                self.output.append(f"{i:3}. {step}")
            self.output.append(f"... and {len(steps) - 20} more steps")
        else:
            for i, step in enumerate(steps, 1):
                self.output.append(f"{i:3}. {step}")

    def valid_dna(self, seq):
        return all(c in "ACGT" for c in seq)
    
    def visualize_step(self, i, j, action):
     self.backtracking_output.append(f"dp[{i}][{j}] → {action}")
     self.backtracking_output.moveCursor(QTextCursor.End)
     QApplication.processEvents()
     time.sleep(0.2)  # Small delay for visualization effect

    def display_dp_table(self, dp, S, T):
        #Display the DP table in a readable QTableWidget.
        n, m = len(S), len(T)
        
        # Set table dimensions: (n+1) rows x (m+1) columns
        self.dp_table_widget.setRowCount(n + 1)
        self.dp_table_widget.setColumnCount(m + 1)
        
        # Set horizontal headers (T sequence)
        horizontal_headers = [''] + list(T)  # Empty cell for (0,0)
        self.dp_table_widget.setHorizontalHeaderLabels(horizontal_headers)
        
        # Set vertical headers (S sequence)
        vertical_headers = [''] + list(S)  # Empty cell for (0,0)
        self.dp_table_widget.setVerticalHeaderLabels(vertical_headers)
        
        # Fill the table with DP values
        for i in range(n + 1):
            for j in range(m + 1):
                item = QTableWidgetItem(str(dp[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Color code based on position
                if i == 0 and j == 0:
                    item.setBackground(Qt.lightGray)  # Starting cell
                elif i == n and j == m:
                    item.setBackground(Qt.yellow)  # Final cell (result)
                
                self.dp_table_widget.setItem(i, j, item)
        
        # Adjust column widths
        self.dp_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dp_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # Add a title/label above the table
        self.dp_table_widget.setToolTip(f"DP Table: Minimum edit distance = {dp[n][m]}")
        
        # Switch to DP table tab
        self.tab_widget.setCurrentIndex(2)

    def display_dp_table_preview(self, dp, S, T, max_size=20):
        """Display a preview of DP table for long sequences."""
        n, m = len(S), len(T)
        
        if n <= max_size and m <= max_size:
            # If sequences are short, show full table
            return self.display_dp_table(dp, S, T)
        
        # For long sequences, show a preview
        self.dp_table_widget.clear()
        preview_n = min(n, max_size)
        preview_m = min(m, max_size)
        
        self.dp_table_widget.setRowCount(preview_n + 2)  # +2 for headers and "..."
        self.dp_table_widget.setColumnCount(preview_m + 2)
        
        # Set headers
        horizontal_headers = [''] + [T[j] for j in range(preview_m)] + ['...']
        vertical_headers = [''] + [S[i] for i in range(preview_n)] + ['...']
        
        self.dp_table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.dp_table_widget.setVerticalHeaderLabels(vertical_headers)
        
        # Fill preview cells
        for i in range(preview_n + 1):
            for j in range(preview_m + 1):
                if i == preview_n or j == preview_m:
                    # Last row/column for "..." indicators
                    item = QTableWidgetItem("..." if i == preview_n and j == preview_m else "")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.dp_table_widget.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(str(dp[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.dp_table_widget.setItem(i, j, item)
        
        # Add full result at bottom right
        result_item = QTableWidgetItem(f"Result: {dp[n][m]}")
        result_item.setTextAlignment(Qt.AlignCenter)
        result_item.setBackground(Qt.yellow)
        self.dp_table_widget.setItem(preview_n + 1, preview_m + 1, result_item)
        
        # Adjust sizes
        self.dp_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dp_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.tab_widget.setCurrentIndex(2)

    def display_dp_table_text(self, dp, S, T):
        """Display a text version of DP table in results tab."""
        n, m = len(S), len(T)
        
        # Only show for small sequences
        if n > 20 or m > 20:
            self.output.append(f"\nDP Table too large to display ({n+1}x{m+1} cells)")
            self.output.append(f"Final edit distance: {dp[n][m]}")
            return
        
        self.output.append("\n" + "="*60)
        self.output.append("DYNAMIC PROGRAMMING TABLE:")
        self.output.append("="*60)
        
        # Create header row
        header = "      " + "  ".join(f"  {char}" for char in T)
        self.output.append(header)
        
        # Create separator
        separator = "    " + "+---" * (m + 1) + "+"
        self.output.append(separator)
        
        # Print each row
        for i in range(n + 1):
            row_str = f"{' ' if i==0 else S[i-1]} {i:2} |"
            for j in range(m + 1):
                row_str += f" {dp[i][j]:2} |"
            self.output.append(row_str)
            self.output.append(separator)
        
        self.output.append(f"\nMinimum edit distance (bottom-right): {dp[n][m]}")

    def read_dna_from_file(self, file_path):
         #Reads a DNA sequence from a file, handling FASTA format.
        try:
            with open(file_path, "r") as f:
                content = f.read().upper()
        
            # Remove FASTA header (lines starting with '>')
            lines = content.split('\n')
            sequence_parts = []
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('>'):  # Skip empty lines and headers
                    continue
                
                # Remove any spaces or numbers from the sequence
                cleaned_line = ''.join([c for c in line if c in 'ACGT'])
                if cleaned_line:
                    sequence_parts.append(cleaned_line)
            
            if not sequence_parts:
                QMessageBox.warning(self, "Error", f"No valid DNA sequence found in {file_path}")
                return ""
            
            return "".join(sequence_parts)
            
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File not found: {file_path}")
            return ""
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error reading {file_path}: {str(e)}")
            return ""
    
    def load_initial_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Mutated DNA File", 
            "", 
            "DNA Files (*.txt *.fasta *.fa);;All Files (*)"
        )
        if file_path:
            self.s_path.setText(file_path)
            # Show a quick preview
            seq = self.read_dna_from_file(file_path)
            if seq:
                self.output.append(f"✓ Loaded mutated DNA: {os.path.basename(file_path)} ({len(seq)} bp)")

    def load_target_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Healthy DNA File", 
            "", 
            "DNA Files (*.txt *.fasta *.fa);;All Files (*)"
        )
        if file_path:
            self.t_path.setText(file_path)
            # Show a quick preview
            seq = self.read_dna_from_file(file_path)
            if seq:
                self.output.append(f"✓ Loaded healthy DNA: {os.path.basename(file_path)} ({len(seq)} bp)")

        



def main():
    app = QApplication(sys.argv)
    window = DNAMutationGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
