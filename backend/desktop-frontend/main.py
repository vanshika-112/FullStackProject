import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QLineEdit, QListWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4))
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop App")
        self.resize(600, 750)

        self.token = None  # JWT access token

        self.initUI()

    def initUI(self):
        with open("styles.css", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.login_label = QLabel("LOGIN")
        self.login_label.setStyleSheet("font-size: 21pt; font-family: Montserrat;")
        self.login_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.login_label)

        # Username
        self.row1 = QHBoxLayout()
        self.user_label = QLabel("Username")
        self.row1.addWidget(self.user_label)
        self.username_input = QLineEdit()
        self.row1.addWidget(self.username_input)
        self.layout.addLayout(self.row1)

        # Password
        self.row2 = QHBoxLayout()
        self.pass_label = QLabel("Password")
        self.row2.addWidget(self.pass_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.row2.addWidget(self.password_input)
        self.layout.addLayout(self.row2)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Status label
        self.status_label = QLabel("Please login!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label) 

        self.layout.addStretch()


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
                json={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                self.access_token = response.json()

                self.token = self.access_token["access"]

                self.status_label.setText("Login successful ✅")

                self.login_success()
                self.load_last_five()
                self.upload_button.setEnabled(True)

            else:
                self.status_label.setText("Login failed ❌")

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

                if "pdf_url" in data:
                    self.pdf_url = data["pdf_url"]
                    self.download_btn.setEnabled(True)

                self.status_label.setText(
                    f"Uploaded | Rows: {data['total_count']}"
                )

                self.load_last_five()

                # Plot chart 
                self.plot_chart(data["equipment_distribution"])

            else:
                self.status_label.setText("Upload failed!")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    # ---------------- PLOT CHART ----------------
    def plot_chart(self, distribution):
        self.canvas.axes.clear()

        labels = list(distribution.keys())
        values = list(distribution.values())

        bars = self.canvas.axes.bar(labels, values)

        self.canvas.axes.set_title("Equipment Type Distribution")
        self.canvas.axes.set_xlabel("Equipment Type")
        self.canvas.axes.set_ylabel("Count")

        self.canvas.axes.tick_params(axis='x', rotation=45)

        for bar in bars:
            height = bar.get_height()
            self.canvas.axes.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(height),
                ha='center',
                va='bottom'
            )

        self.canvas.draw()

    def load_last_five(self):
        if not hasattr(self, "access_token"):
            return

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(
            "http://127.0.0.1:8000/api/datasets/last-five/",
            headers=headers
        )

        if response.status_code == 200:
            self.history_list.clear()

            for item in response.json():
                filename = item["file"].split("/")[-1]
                uploaded_at = item["uploaded_at"]

                self.history_list.addItem(
                    f"{filename}  |  {uploaded_at}"
                )
        
    def download_pdf(self):
        if hasattr(self, "pdf_url"):
            import webbrowser
            webbrowser.open(self.pdf_url)

    def login_success(self):
        self.username_input.hide()
        self.password_input.hide()
        self.login_button.hide()
        self.status_label.hide()
        self.user_label.hide()
        self.pass_label.hide()
        self.login_label.hide()

        self.dashboard_label = QLabel("DASHBOARD")
        self.dashboard_label.setStyleSheet("font-size: 21pt; font-family: Montserrat;")
        self.dashboard_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dashboard_label)

        # Upload button
        self.row3 = QHBoxLayout()
        self.upload_label = QLabel("Upload your csv file here!")
        self.row3.addWidget(self.upload_label)
        self.upload_button = QPushButton("Upload")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.open_file)
        self.row3.addWidget(self.upload_button)
        self.layout.addLayout(self.row3)

        #history button
        self.history_label = QLabel("Last 5 Uploads")
        self.layout.addWidget(self.history_label)
        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)

        # Chart canvas
        self.canvas = MplCanvas(self)
        self.layout.addWidget(self.canvas)

        #Download button 
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_pdf)
        self.layout.addWidget(self.download_btn)

        self.setLayout(self.layout)



# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())