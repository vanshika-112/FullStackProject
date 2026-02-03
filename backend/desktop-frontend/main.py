import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
import matplotlib.pyplot as plt
import pandas as pd

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "CSV Analyzer"
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Upload a CSV file:")
        self.layout.addWidget(self.label)
        
        self.button = QPushButton("Select CSV")
        self.button.clicked.connect(self.open_file)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
        self.show()
    
    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.label.setText(f"Selected: {file_path}")
            self.analyze_csv(file_path)
    
    def analyze_csv(self, file_path):
        df = pd.read_csv(file_path)
        print("Total rows:", len(df))
        print("Averages:\n", df.mean(numeric_only=True))
        if 'equipment_type' in df.columns:
            print("Equipment distribution:\n", df['equipment_type'].value_counts())
        
        # Plot example
        if 'equipment_type' in df.columns:
            df['equipment_type'].value_counts().plot(kind='bar')
            plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
