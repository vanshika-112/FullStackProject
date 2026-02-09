import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QFileDialog, QLabel, QLineEdit
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Analyzer Desktop App")
        self.setGeometry(200, 200, 400, 300)

        self.token = None  # JWT access token

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Username
        self.username_label = QLabel("Username")
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Status label
        self.status_label = QLabel("Please login")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Upload button (disabled until login)
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.open_file)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)

    # ---------------- LOGIN ----------------
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.status_label.setText("Enter username and password")
            return

        url = "http://127.0.0.1:8000/api/token/"

        try:
            response = requests.post(
                url,
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.token = response.json()["access"]
                self.status_label.setText("Login successful!")
                self.upload_button.setEnabled(True)
            else:
                self.status_label.setText("Login failed!")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    # ---------------- FILE PICKER ----------------
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            self.upload_csv(file_path)

    # ---------------- CSV UPLOAD ----------------
    def upload_csv(self, file_path):
        if not self.token:
            self.status_label.setText("Login required")
            return

        url = "http://127.0.0.1:8000/api/upload/"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        files = {
            "file": open(file_path, "rb")
        }

        try:
            response = requests.post(url, headers=headers, files=files)

            if response.status_code == 201:
                data = response.json()
                self.status_label.setText(
                    f"Uploaded ✅ | Rows: {data['total_count']}"
                )

                # Print results in terminal (for now)
                print("Total Count:", data["total_count"])
                print("Averages:", data["averages"])
                print("Equipment Distribution:", data["equipment_distribution"])

            else:
                self.status_label.setText("Upload failed!")
                print(response.text)

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
