"""
DNA Mutation Pathway Reconstruction GUI
A professional interface for analyzing DNA mutation pathways using dynamic programming.
"""

import sys
import os
import time
# Import PyQt5 widgets for GUI components
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QMessageBox,
    QHBoxLayout, QGroupBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QProgressBar
)
# Import PyQt5 graphical elements for styling
from PyQt5.QtGui import QTextCursor, QFont, QPalette, QColor
# Import PyQt5 core modules for events and timers
from PyQt5.QtCore import Qt, QTimer

# Import custom modules for DNA analysis algorithms
from dp_model import compute_dp_table  # Dynamic programming table computation
from backtracking import reconstruct_path  # Pathway reconstruction algorithm
from visualization import print_dp_table  # Table visualization helper


class DNAMutationGUI(QWidget):
    """Main GUI window for DNA Mutation Pathway Analysis"""
    
    def __init__(self):
        # Initialize parent QWidget class
        super().__init__()
        # Set up user interface components
        self.setup_ui()
        # Apply visual styling to the interface
        self.setup_styles()
        
    def setup_ui(self):
        """Initialize and arrange all UI components"""
        # Set window title with DNA emoji
        self.setWindowTitle("🧬 DNA Mutation Pathway Analyzer")
        # Set window position (x, y) and size (width, height)
        self.setGeometry(300, 200, 900, 700)
        
        # Main layout - vertical box layout for overall structure
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)  # Space between widgets
        main_layout.setContentsMargins(20, 20, 20, 20)  # Margins around edges
        
        # Header label with application title
        header_label = QLabel("DNA Mutation Pathway Reconstruction")
        header_label.setObjectName("header")  # For CSS styling
        header_label.setAlignment(Qt.AlignCenter)  # Center align text
        main_layout.addWidget(header_label)
        
        # File selection group box
        file_group = QGroupBox("DNA Sequence Input")
        file_layout = QVBoxLayout()  # Vertical layout for file inputs
        
        # Mutated DNA file selection section
        s_layout = QHBoxLayout()  # Horizontal layout for file selection row
        s_layout.addWidget(QLabel("Mutated DNA:"))  # Label for mutated DNA
        self.s_path = QLineEdit()  # Text field for file path
        self.s_path.setPlaceholderText("Select mutated DNA file...")  # Hint text
        self.s_path.setReadOnly(True)  # Prevent manual editing
        s_layout.addWidget(self.s_path, 1)  # Add with stretch factor
        self.s_btn = QPushButton("📁 Browse")  # Browse button with folder icon
        self.s_btn.clicked.connect(self.load_initial_file)  # Connect button click to handler
        s_layout.addWidget(self.s_btn)
        file_layout.addLayout(s_layout)  # Add horizontal layout to vertical layout
        
        # Healthy DNA file selection section
        t_layout = QHBoxLayout()  # Horizontal layout for file selection row
        t_layout.addWidget(QLabel("Healthy DNA:"))  # Label for healthy DNA
        self.t_path = QLineEdit()  # Text field for file path
        self.t_path.setPlaceholderText("Select healthy DNA file...")  # Hint text
        self.t_path.setReadOnly(True)  # Prevent manual editing
        t_layout.addWidget(self.t_path, 1)  # Add with stretch factor
        self.t_btn = QPushButton("📁 Browse")  # Browse button with folder icon
        self.t_btn.clicked.connect(self.load_target_file)  # Connect button click to handler
        t_layout.addWidget(self.t_btn)
        file_layout.addLayout(t_layout)
        
        # Preview label to show loaded sequence info
        self.preview_label = QLabel("")
        self.preview_label.setWordWrap(True)  # Allow text to wrap to next line
        file_layout.addWidget(self.preview_label)
        
        # Set layout for file group and add to main layout
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Progress bar for showing analysis progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # Hidden by default
        main_layout.addWidget(self.progress_bar)
        
        # Run analysis button section
        button_layout = QHBoxLayout()  # Horizontal layout for button
        self.run_btn = QPushButton("🔬 Analyze Mutation Pathway")
        self.run_btn.setObjectName("runButton")  # For special CSS styling
        self.run_btn.clicked.connect(self.run_dp)  # Connect to analysis function
        button_layout.addWidget(self.run_btn)
        main_layout.addLayout(button_layout)
        
        # Tab widget for organizing different views of results
        self.tab_widget = QTabWidget()
        
        # Tab 1: Summary Results
        self.results_tab = QWidget()
        results_layout = QVBoxLayout()
        self.output = QTextEdit()  # Main output display
        self.output.setReadOnly(True)  # Prevent editing
        self.output.setFont(QFont("Courier New", 10))  # Monospace font for alignment
        results_layout.addWidget(self.output)
        self.results_tab.setLayout(results_layout)
        
        # Tab 2: Step-by-Step Reconstruction
        self.backtracking_tab = QWidget()
        backtracking_layout = QVBoxLayout()
        backtracking_header = QLabel("Backtracking Steps:")
        backtracking_header.setObjectName("tabHeader")  # For CSS styling
        backtracking_layout.addWidget(backtracking_header)
        self.backtracking_output = QTextEdit()  # Backtracking steps display
        self.backtracking_output.setReadOnly(True)  # Prevent editing
        self.backtracking_output.setFont(QFont("Courier New", 9))  # Monospace font
        backtracking_layout.addWidget(self.backtracking_output)
        self.backtracking_tab.setLayout(backtracking_layout)
        
        # Tab 3: DP Table Visualization
        self.dp_table_tab = QWidget()
        dp_table_layout = QVBoxLayout()
        dp_table_header = QLabel("Dynamic Programming Table:")
        dp_table_header.setObjectName("tabHeader")  # For CSS styling
        dp_table_layout.addWidget(dp_table_header)
        self.dp_table_widget = QTableWidget()  # Table for DP matrix visualization
        self.dp_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        self.dp_table_widget.setAlternatingRowColors(True)  # Zebra striping
        # Custom CSS styling for table
        self.dp_table_widget.setStyleSheet("""
            QTableWidget {
                gridline-color: #cccccc;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        dp_table_layout.addWidget(self.dp_table_widget)
        self.dp_table_tab.setLayout(dp_table_layout)
        
        # Add all tabs to tab widget with icons and names
        self.tab_widget.addTab(self.results_tab, "📊 Summary")
        self.tab_widget.addTab(self.backtracking_tab, "🔍 Step-by-Step")
        self.tab_widget.addTab(self.dp_table_tab, "📈 DP Table")
        
        # Add tab widget to main layout with stretch factor
        main_layout.addWidget(self.tab_widget, 1)
        
        # Status bar at bottom for messages
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")  # For CSS styling
        main_layout.addWidget(self.status_label)
        
        # Set main layout for the window
        self.setLayout(main_layout)
        
    def setup_styles(self):
        """Apply professional styling to the GUI using CSS"""
        self.setStyleSheet("""
            /* Base widget styling */
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Group box styling */
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2E7D32;
            }
            
            /* Header label styling */
            QLabel#header {
                font-size: 20px;
                font-weight: bold;
                color: #1565C0;
                padding: 10px;
            }
            
            /* Tab header styling */
            QLabel#tabHeader {
                font-size: 14px;
                font-weight: bold;
                color: #1976D2;
                padding: 5px;
            }
            
            /* Button styling */
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            
            /* Special run button styling */
            QPushButton#runButton {
                background-color: #4CAF50;
                font-size: 14px;
                padding: 10px 20px;
            }
            
            QPushButton#runButton:hover {
                background-color: #388E3C;
            }
            
            /* Text input styling */
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            
            /* Text display area styling */
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            
            /* Tab widget styling */
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                font-weight: bold;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #f0f0f0;
            }
            
            /* Progress bar styling */
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            
            /* Status label styling */
            QLabel#statusLabel {
                color: #666;
                font-style: italic;
                padding: 5px;
                border-top: 1px solid #ddd;
            }
            
            /* Table widget selection styling */
            QTableWidget {
                selection-background-color: #E3F2FD;
            }
        """)
        
    def update_status(self, message, color="black"):
        """Update status bar message with color coding"""
        self.status_label.setText(message)  # Set message text
        # Apply CSS based on message type
        if color == "error":
            self.status_label.setStyleSheet("color: #D32F2F; font-style: normal; font-weight: bold;")
        elif color == "success":
            self.status_label.setStyleSheet("color: #388E3C; font-style: normal; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #666; font-style: italic;")
            
    def load_initial_file(self):
        """Load mutated DNA file from file system"""
        # Open file dialog for selecting mutated DNA file
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Mutated DNA File", 
            "", 
            "DNA Files (*.txt *.fasta *.fa);;All Files (*)"
        )
        # If user selected a file
        if file_path:
            self.s_path.setText(file_path)  # Display file path in text field
            # Read DNA sequence from file
            seq = self.read_dna_from_file(file_path)
            if seq:
                # Update preview with file info and sequence snippet
                self.preview_label.setText(
                    f"✓ <b>Mutated DNA loaded:</b> {os.path.basename(file_path)} "
                    f"({len(seq):,} bp, first 50: {seq[:50]}...)"
                )
                # Update status bar with success message
                self.update_status(f"Loaded mutated DNA: {os.path.basename(file_path)}", "success")
                
    def load_target_file(self):
        """Load healthy DNA file from file system"""
        # Open file dialog for selecting healthy DNA file
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Healthy DNA File", 
            "", 
            "DNA Files (*.txt *.fasta *.fa);;All Files (*)"
        )
        # If user selected a file
        if file_path:
            self.t_path.setText(file_path)  # Display file path in text field
            # Read DNA sequence from file
            seq = self.read_dna_from_file(file_path)
            if seq:
                # Update preview with file info and sequence snippet
                self.preview_label.setText(
                    f"✓ <b>Healthy DNA loaded:</b> {os.path.basename(file_path)} "
                    f"({len(seq):,} bp, first 50: {seq[:50]}...)"
                )
                # Update status bar with success message
                self.update_status(f"Loaded healthy DNA: {os.path.basename(file_path)}", "success")
                
    def run_dp(self):
        """Execute dynamic programming analysis on DNA sequences"""
        # Clear previous results from all displays
        self.output.clear()
        self.backtracking_output.clear()
        
        # Validate that both files have been selected
        if not self.s_path.text() or not self.t_path.text():
            QMessageBox.warning(self, "Input Error", 
                              "Please select both DNA files before running analysis.")
            return
        
        # Read DNA sequences from selected files
        S = self.read_dna_from_file(self.s_path.text())  # Mutated DNA
        T = self.read_dna_from_file(self.t_path.text())  # Healthy DNA
        
        # Check if sequences were read successfully
        if not S or not T:
            self.update_status("Error reading DNA sequences", "error")
            return
        
        # Validate DNA sequences contain only valid characters (A, C, G, T)
        if not self.valid_dna(S):
            # Find invalid characters in mutated DNA
            invalid_chars = ''.join(sorted(set(c for c in S if c not in "ACGT")))
            QMessageBox.warning(self, "Invalid DNA Sequence", 
                              f"Mutated DNA contains invalid characters: {invalid_chars}")
            return
        
        if not self.valid_dna(T):
            # Find invalid characters in healthy DNA
            invalid_chars = ''.join(sorted(set(c for c in T if c not in "ACGT")))
            QMessageBox.warning(self, "Invalid DNA Sequence", 
                              f"Healthy DNA contains invalid characters: {invalid_chars}")
            return
        
        # Setup UI for processing (show progress bar)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress (spinning)
        self.update_status("Processing... Please wait", "black")
        QApplication.processEvents()  # Update UI immediately
        
        # Run dynamic programming analysis
        try:
            # Compute DP table with substitution cost 2, indel cost 2, match cost -1
            dp, choice = compute_dp_table(S, T, 2, 2, 1)
            # Display results in GUI
            self.display_results(S, T, dp, choice)
        except Exception as e:
            # Handle any errors during analysis
            self.update_status(f"Analysis error: {str(e)}", "error")
            QMessageBox.critical(self, "Analysis Error", 
                               f"An error occurred during analysis:\n{str(e)}")
        finally:
            # Hide progress bar when done (whether success or error)
            self.progress_bar.setVisible(False)
            
    def display_results(self, S, T, dp, choice):
        """Display all analysis results in appropriate tabs"""
        # Switch to results tab to show summary
        self.tab_widget.setCurrentIndex(0)
        
        # Display header and sequence info in output area
        self.output.append("╔══════════════════════════════════════════════════════════════════╗")
        self.output.append("║                     DNA MUTATION PATHWAY ANALYSIS                ║")
        self.output.append("╚══════════════════════════════════════════════════════════════════╝")
        self.output.append("")
        
        # Display sequence information
        self.output.append("📊 SEQUENCE INFORMATION")
        self.output.append("═" * 60)  # Separator line
        self.output.append(f"🔹 Mutated DNA Length: {len(S):,} base pairs")
        self.output.append(f"🔹 Healthy DNA Length:  {len(T):,} base pairs")
        self.output.append("")
        
        # Display sequence preview (first 100 base pairs)
        self.output.append("👁️ SEQUENCE PREVIEW (First 100 bp)")
        self.output.append("─" * 60)  # Separator line
        self.output.append(f"Mutated: {S[:100]}")
        self.output.append(f"Healthy: {T[:100]}")
        self.output.append("")
        
        # Display DP table in text format (for small sequences)
        self.display_dp_table_text(dp, S, T)
        
        # Display minimum mutation cost
        self.output.append("🎯 ANALYSIS RESULTS")
        self.output.append("═" * 60)
        min_distance = dp[len(S)][len(T)]  # Bottom-right cell contains final cost
        self.output.append(f"✅ Minimum mutation cost: {min_distance}")
        self.output.append("")
        
        # Reconstruct mutation pathway using backtracking
        self.update_status("Reconstructing mutation pathway...", "black")
        # Call reconstruct_path with visual callback for step-by-step display
        steps = reconstruct_path(choice, S, T, verbose=False, 
                                visual_callback=self.visualize_step)
        
        # Count different types of mutations
        sub_count = sum(1 for step in steps if "Substitute" in step)
        ins_count = sum(1 for step in steps if "Insert" in step)
        del_count = sum(1 for step in steps if "Delete" in step)
        
        # Display mutation statistics
        self.output.append("📈 MUTATION STATISTICS")
        self.output.append("─" * 60)
        self.output.append(f"Total Operations: {len(steps):,}")
        self.output.append(f"  • Substitutions: {sub_count:,}")
        self.output.append(f"  • Insertions:    {ins_count:,}")
        self.output.append(f"  • Deletions:     {del_count:,}")
        self.output.append("")
        
        # Display mutation pathway steps
        self.output.append("🔄 MUTATION PATHWAY")
        self.output.append("─" * 60)
        
        # Limit display to first 20 steps if pathway is long
        if len(steps) > 20:
            self.output.append(f"Displaying first 20 of {len(steps)} steps:")
            for i, step in enumerate(steps[:20], 1):
                self.output.append(f"{i:3}. {step}")
            self.output.append(f"... and {len(steps) - 20} more steps")
        else:
            # Display all steps if 20 or fewer
            for i, step in enumerate(steps, 1):
                self.output.append(f"{i:3}. {step}")
        
        # Display DP table in table widget (visual representation)
        if len(S) <= 40 and len(T) <= 40:
            # Show full table for small sequences
            self.display_dp_table(dp, S, T)
        else:
            # Show preview for large sequences
            self.display_dp_table_preview(dp, S, T, max_size=15)
        
        # Update status bar with completion message
        self.update_status(f"Analysis complete - mutation cost: {min_distance}", "success")
        
    def visualize_step(self, i, j, action):
        """Visualize backtracking steps with highlighting in the backtracking tab"""
        # Append step information to backtracking output
        self.backtracking_output.append(f"📍 dp[{i}][{j}] → {action}")
        # Scroll to bottom to show latest step
        self.backtracking_output.moveCursor(QTextCursor.End)
        # Process GUI events to update display immediately
        QApplication.processEvents()
        # Small delay for visualization effect
        time.sleep(0.1)
        
    def display_dp_table(self, dp, S, T):
        """Display the full DP table in QTableWidget for small sequences"""
        n, m = len(S), len(T)  # Get sequence lengths
        
        # Set table dimensions (n+1 rows, m+1 columns for DP matrix)
        self.dp_table_widget.setRowCount(n + 1)
        self.dp_table_widget.setColumnCount(m + 1)
        
        # Set headers with DNA characters and indices
        horizontal_headers = [''] + list(T)  # Column headers: empty + T sequence
        vertical_headers = [''] + list(S)    # Row headers: empty + S sequence
        
        self.dp_table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.dp_table_widget.setVerticalHeaderLabels(vertical_headers)
        
        # Find maximum value for color scaling
        max_val = max(max(row) for row in dp)
        
        # Fill table cells with DP values and color coding
        for i in range(n + 1):
            for j in range(m + 1):
                item = QTableWidgetItem(str(dp[i][j]))
                item.setTextAlignment(Qt.AlignCenter)  # Center text in cell
                
                # Color gradient based on DP value
                value = dp[i][j]
                intensity = min(255, 255 - (value * 50))
                
                # Special cells with unique coloring
                if i == 0 and j == 0:
                    item.setBackground(QColor(220, 237, 200))  # Start cell - light green
                    item.setForeground(QColor(0, 0, 0))
                elif i == n and j == m:
                    item.setBackground(QColor(255, 243, 205))  # Result cell - light yellow
                    item.setForeground(QColor(0, 0, 0))
                    item.setFont(QFont("Arial", 10, QFont.Bold))  # Bold for result
                else:
                    # Gradient from white to blue based on value
                    red = 240 - (value * 20)
                    green = 245 - (value * 30)
                    blue = 255
                    item.setBackground(QColor(red, green, blue))
                    item.setForeground(QColor(0, 0, 0))
                
                # Add item to table
                self.dp_table_widget.setItem(i, j, item)
        
        # Add zebra striping for readability
        self.dp_table_widget.setAlternatingRowColors(True)
        
        # Adjust column and row sizes
        header = self.dp_table_widget.horizontalHeader()
        header.setDefaultSectionSize(40)  # Default column width
        header.setMinimumSectionSize(30)  # Minimum column width
        
        vheader = self.dp_table_widget.verticalHeader()
        vheader.setDefaultSectionSize(40)  # Default row height
        vheader.setMinimumSectionSize(30)  # Minimum row height
        
        # Resize columns and rows to fit contents
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        
    def display_dp_table_preview(self, dp, S, T, max_size=20):
        """Display preview of DP table for large sequences"""
        n, m = len(S), len(T)  # Get sequence lengths
        
        # If sequences are small enough, show full table
        if n <= max_size and m <= max_size:
            return self.display_dp_table(dp, S, T)
        
        # Calculate preview dimensions
        preview_n = min(n, max_size)
        preview_m = min(m, max_size)
        
        # Set table dimensions with +2 for ellipsis rows/columns
        self.dp_table_widget.setRowCount(preview_n + 2)
        self.dp_table_widget.setColumnCount(preview_m + 2)
        
        # Set headers with ellipsis for truncated sequences
        horizontal_headers = [''] + [T[j] for j in range(preview_m)] + ['⋯']
        vertical_headers = [''] + [S[i] for i in range(preview_n)] + ['⋯']
        
        self.dp_table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.dp_table_widget.setVerticalHeaderLabels(vertical_headers)
        
        # Fill preview cells
        for i in range(preview_n + 1):
            for j in range(preview_m + 1):
                if i == preview_n or j == preview_m:
                    # Add ellipsis in bottom-right corner
                    item = QTableWidgetItem("⋯" if i == preview_n and j == preview_m else "")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.dp_table_widget.setItem(i, j, item)
                else:
                    # Add DP value for preview region
                    item = QTableWidgetItem(str(dp[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.dp_table_widget.setItem(i, j, item)
        
        # Show final result in special cell
        result_item = QTableWidgetItem(f"Result: {dp[n][m]}")
        result_item.setTextAlignment(Qt.AlignCenter)
        result_item.setBackground(QColor(255, 255, 200))  # Light yellow background
        self.dp_table_widget.setItem(preview_n + 1, preview_m + 1, result_item)
        
        # Auto-resize columns and rows
        self.dp_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dp_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
    def display_dp_table_text(self, dp, S, T):
        """Display text version of DP table in results tab"""
        n, m = len(S), len(T)  # Get sequence lengths
        
        # For large sequences, show only preview
        if n > 20 or m > 20:
            self.output.append("📐 DP TABLE (Preview)")
            self.output.append("─" * 60)
            self.output.append(f"Table dimensions: {n+1} × {m+1} cells")
            self.output.append(f"Final mutation cost: {dp[n][m]}")
            return
        
        # For small sequences, display full table in text format
        self.output.append("📐 DYNAMIC PROGRAMMING TABLE")
        self.output.append("═" * 60)
        
        # Create header row with T sequence characters
        header = "      " + "  ".join(f"  {char}" for char in T)
        self.output.append(header)
        
        # Create separator line
        separator = "    " + "+---" * (m + 1) + "+"
        self.output.append(separator)
        
        # Print each row of DP table
        for i in range(n + 1):
            # Row label with S character (or empty for row 0)
            row_str = f"{' ' if i==0 else S[i-1]} {i:2} |"
            # Add DP values for each column
            for j in range(m + 1):
                row_str += f" {dp[i][j]:2} |"
            self.output.append(row_str)
            self.output.append(separator)  # Separator after each row
        
        # Display final mutation cost
        self.output.append(f"\nMinimum mutation cost: {dp[n][m]}")
        self.output.append("")
        
    def valid_dna(self, seq):
        """Validate DNA sequence contains only ACGT characters"""
        # Check all characters are valid DNA bases
        return all(c in "ACGT" for c in seq)
    
    def read_dna_from_file(self, file_path):
        """Read DNA sequence from file, handling FASTA format"""
        try:
            # Read file content and convert to uppercase
            with open(file_path, "r") as f:
                content = f.read().upper()
            
            # Split into lines and process
            lines = content.split('\n')
            sequence_parts = []  # Store valid DNA segments
            
            for line in lines:
                line = line.strip()  # Remove whitespace
                # Skip empty lines and FASTA headers (starting with '>')
                if not line or line.startswith('>'):
                    continue
                
                # Extract only valid DNA characters
                cleaned_line = ''.join([c for c in line if c in 'ACGT'])
                if cleaned_line:
                    sequence_parts.append(cleaned_line)
            
            # Check if any valid DNA was found
            if not sequence_parts:
                QMessageBox.warning(self, "Error", 
                                  f"No valid DNA sequence found in {os.path.basename(file_path)}")
                return ""
            
            # Combine all valid parts into single sequence
            return "".join(sequence_parts)
            
        except FileNotFoundError:
            # Handle file not found error
            QMessageBox.warning(self, "Error", 
                              f"File not found: {os.path.basename(file_path)}")
            return ""
        except Exception as e:
            # Handle any other file reading errors
            QMessageBox.warning(self, "Error", 
                              f"Error reading {os.path.basename(file_path)}: {str(e)}")
            return ""


def main():
    """Application entry point"""
    # Create QApplication instance (required for PyQt)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use modern Fusion style
    
    # Create and show main window
    window = DNAMutationGUI()
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())


# Standard Python idiom for running as script
if __name__ == "__main__":
    main()