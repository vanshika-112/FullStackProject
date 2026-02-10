# FullStackProject
<h2>Data Analysis & Visualization Platform</h2>

<p>A full-stack application that allows users to upload CSV datasets, analyze data, visualize insights through charts, generate PDF reports, and access the system via both a web interface and a desktop application.</p>

<p>
  <h4>Features</h4>
  1. Authentication
      -> JWT-based login system
      -> Secure API endpoints
      -> Shared authentication for web and desktop apps
  2. Dataset Upload
      -> Upload CSV files
      -> Automatically keeps only the last 5 uploads per user
      -> Old datasets are deleted automatically
  3. Data Analysis
      -> Total record count
      -> Column-wise averages
      -> Equipment/type distribution
      -> Processed on the backend using Django
  4. Visualizations
      -> Equipment/type distribution graphs
      -> Summary displayed in both Web & Desktop apps
  5. PDF Report
      -> Automatically generated after upload
      -> Downloadable from both Web and Desktop applications
  6. Multi-Platform Access
      -> Web App: React
      -> Desktop App: PyQt5
      -> Backend API: Django + Django REST Framework
</p>
<p>
  <h4>Tech Stack</h4>
    <h5>Backend</h5>
    <ul>
      <li>xPython</li>
      <li>Django</li>
      <li>Django REST Framework</li>
      <li>JWT Authentication</li>
      <li>SQLite</li>
      <li>ReportLab (PDF generation)</li>
    </ul>
    <h5>Web Frontend</h5>
    <ul>
      <li>React</li>
      <li>Axios</li>
      <li>Chart.js</li>
      <li>CSS</li>
    </ul>
    <h5>Desktop App</h5>
    <ul>
      <li>PyQt5</li>
      <li>Requests</li>
      <li>Matplotlib (for charts)</li>
    </ul>
</p>
<p>
  <h4>Project Structure</h4>
  <p>
    FullStackProject/
    │
    ├── backend/
    │   ├── backend/            # Django project settings
    │   ├── api/                # API app (upload, analysis, auth)
    │   ├── media/              # Uploaded datasets & generated PDFs
    │   ├── manage.py
    │
    ├── web/                    # React web app
    │   ├── src/
    │   ├── public/
    │   └── package.json
    │
    ├── desktop_frontend/            # PyQt5 application
    │   └── main.py
    │
    └── README.md
  </p>
</p>
<p>
<h4> Setup Instructions</h4>
  <p>
    1️. Backend Setup
    cd backend
    python -m venv venv
    venv\Scripts\activate   # Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    <br>
    Backend runs at:
    http://127.0.0.1:8000/
    <br>
    2️. React Web App Setup
    cd web
    npm install
    npm start
    <br>
    Web app runs at:
    http://localhost:3000/
    <br>
    3️. PyQt Desktop App
    cd desktop_frontend
    python main.py
</p>

<h4>API Endpoints (Core)</h4>
  <pre>
    Endpoint	                         Method         	Description
    /api/token/	                        POST	          Login (JWT)
    /api/token/refresh/                	POST 	         Refresh token
    /api/upload/	                      POST	          Upload CSV
    /api/datasets/last-five/	          GET          	Last 5 uploads
    /media/reports/report.pdf         	GET          	Generated PDF
  </pre>
  
<h4>Authentication Flow</h4>
  <p>
    ->User logs in
    ->Backend returns JWT access & refresh tokens
    ->Token stored in local storage (web) / memory (desktop)
    ->Token sent in Authorization: Bearer <token> header
  </p>
</p>
