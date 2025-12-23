import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QTextCursor

from dp_model import compute_dp_table
from backtracking import reconstruct_path


class DNAMutationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNA Mutation Pathway Reconstruction (DP)")
        self.setGeometry(300, 200, 600, 450)
        self.setup_ui()

    def setup_ui(self):
        self.label_s = QLabel("Initial DNA Sequence:")
        self.input_s = QLineEdit()

        self.label_t = QLabel("Target DNA Sequence:")
        self.input_t = QLineEdit()

        self.run_btn = QPushButton("Run Dynamic Programming")
        self.run_btn.clicked.connect(self.run_dp)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label_s)
        layout.addWidget(self.input_s)
        layout.addWidget(self.label_t)
        layout.addWidget(self.input_t)
        layout.addWidget(self.run_btn)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.output)
        self.backtracking_output = QTextEdit()
        self.backtracking_output.setReadOnly(True)
        layout.addWidget(QLabel("Backtracking Steps:"))
        layout.addWidget(self.backtracking_output)


        self.setLayout(layout)

    def run_dp(self):
        S = self.input_s.text().strip().upper()
        T = self.input_t.text().strip().upper()

        if not S or not T:
            QMessageBox.warning(self, "Error", "Both DNA sequences are required.")
            return

        if not self.valid_dna(S) or not self.valid_dna(T):
            QMessageBox.warning(self, "Error", "DNA must contain only A, C, G, T.")
            return

        dp, choice = compute_dp_table(S, T, 1, 1, 2)
    
        self.output.clear()
        self.output.append(f"Initial DNA: {S}")
        self.output.append(f"Target DNA:  {T}\n")
        self.output.append(f"Minimum Mutation Cost: {dp[len(S)][len(T)]}\n")
        self.output.append("Mutation Path:")
        steps = reconstruct_path(choice,S,T,verbose=False,visual_callback=self.visualize_step)

        for step in steps:
            self.output.append(f"• {step}")

    def valid_dna(self, seq):
        return all(c in "ACGT" for c in seq)
    
    def visualize_step(self, i, j, action):
     self.backtracking_output.append(f"dp[{i}][{j}] → {action}")
     self.backtracking_output.moveCursor(QTextCursor.End)
     QApplication.processEvents()
     time.sleep(0.2)  # Small delay for visualization effect



def main():
    app = QApplication(sys.argv)
    window = DNAMutationGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
