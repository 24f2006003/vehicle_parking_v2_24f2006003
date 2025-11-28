# Vehicle Parking Management System

## Description
A comprehensive web application for managing vehicle parking, featuring role-based access for Admins and Users. The system handles parking lot creation, spot allocation, reservations, and provides analytical dashboards with automated email reminders and reports.

## Technologies Used
- **Flask (Python)**: Core backend framework for API development.
- **Vue.js (JavaScript)**: Frontend framework for building a dynamic and responsive UI.
- **Bootstrap 5**: CSS framework for styling and responsive design (No custom CSS libraries used).
- **SQLite**: Relational database for storing user, parking lot, and reservation data.
- **Redis**: In-memory data structure store used for caching and as a message broker for Celery.
- **Celery**: Distributed task queue for handling background jobs like daily reminders and monthly reports.
- **Flask-JWT-Extended**: For secure token-based authentication.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-Mail**: For sending email notifications.

## DB Schema Design

<img width="835" height="680" alt="Vehicle-Parking-DBDiagram" src="https://github.com/user-attachments/assets/aaa6a782-4ddb-41a6-a674-c3ae5f7ff72e" />

### Users Table
- `id`: Integer, Primary Key
- `username`: Text, Unique, Not Null
- `email`: Text, Unique, Not Null
- `password`: Text, Not Null
- `role`: Text, Default 'user' (Constraints: 'admin' or 'user')

### ParkingLot Table
- `id`: Integer, Primary Key
- `prime_location_name`: Text, Not Null
- `price`: Float, Not Null
- `address`: Text, Not Null
- `pin_code`: Integer, Not Null
- `number_of_spots`: Integer, Not Null
- `available_spots`: Integer, Not Null

### ParkingSpot Table
- `id`: Integer, Primary Key
- `lot_id`: Integer, ForeignKey('parking_lot.id')
- `status`: String(1), Default 'A' (Constraints: 'A'=Available, 'O'=Occupied)

### Reservation Table
- `id`: Integer, Primary Key
- `spot_id`: Integer, ForeignKey('parking_spot.id')
- `user_id`: Integer, ForeignKey('user.id')
- `parking_timestamp`: DateTime, Not Null
- `leaving_timestamp`: DateTime, Nullable
- `parking_cost`: Float, Nullable
- `vehicle_number`: Text, Nullable
- `status`: Text, Default 'active' (Constraints: 'active', 'completed', 'cancelled')

**Design Rationale**: The schema is normalized to separate concerns. `ParkingLot` manages static lot info, while `ParkingSpot` tracks individual spot status. `Reservation` links users to spots with time tracking, allowing for historical data analysis and billing.

## API Design
The API is designed using RESTful principles. It exposes endpoints for authentication, resource management (Lots, Spots, Users), and business logic (Reservations, Reporting).
- **Authentication**: `/api/login`, `/api/register`
- **Resources**: `/api/lots`, `/api/users`, `/api/reservations`
- **Jobs**: `/api/export_csv`, `/api/daily_reminder`, `/api/monthly_report`

*Please refer to the `api.yaml` file for the complete OpenAPI specification.*

## Architecture and Features
**Organization**:
- **Backend**: Follows a modular structure. `application/models.py` defines the DB schema, `application/routes.py` contains the API controllers, and `application/tasks.py` handles background jobs. Configuration is separated in `config.py`.
- **Frontend**: Built with Vue.js components organized by role (`components/admin`, `components/user`). `routes.js` manages client-side routing with navigation guards for role protection.

**Features Implemented**:
- **Role-Based Access Control**: Secure login for Admins and Users.
- **Parking Management**: Admins can create lots; spots are auto-generated.
- **Reservation System**: Users can book available spots; system handles auto-allocation.
- **Dashboard Analytics**: Visual summaries for both Admins (occupancy) and Users (spending/history).
- **Background Jobs**:
    - **Daily Reminders**: Checks for inactivity and sends email alerts.
    - **Monthly Reports**: Generates and emails HTML activity reports.
    - **CSV Export**: Asynchronous job to export user parking history.
- **Performance**: Redis caching implemented for dashboard statistics to reduce DB load.

## Project Video Demonstration
[Insert Google Drive Video Link Here]

## How to Run

### Prerequisites
Ensure the following are installed on your system:
- **Python 3.8+**
- **Node.js** (v16+ recommended) & **npm**
- **Redis** (Must be installed and running)
- **Git**
- **WSL** (Recommended for Windows users to run Redis/Celery)

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/24f2006003/vehicle_parking_v2_24f2006003.git
cd mad2-project-vehicle-parking
```

#### 2. Backend Setup
Open a terminal (WSL recommended) and navigate to the backend directory:
```bash
cd backend
```

**Create and Activate Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows Powershell: venv\Scripts\activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start Redis Server:**
```bash
sudo service redis-server start
# Verify it's running:
redis-cli ping  # Should return 'PONG'
```

**Start Celery Worker (Terminal 2):**
In a new terminal (inside `backend` folder, with venv activated):
```bash
celery -A app.celery worker --loglevel=info
```

**Start Celery Beat (Terminal 3):**
In a new terminal (inside `backend` folder, with venv activated):
```bash
celery -A app.celery beat --loglevel=info
```

**Start Flask Application (Terminal 1):**
Back in the first terminal:
```bash
python app.py
```
The backend will run at `http://127.0.0.1:5000`.

#### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

**Install Dependencies:**
```bash
npm install
```

**Run Development Server:**
```bash
npm run dev
```
The frontend will run at `http://localhost:5173` (or similar).

#### 4. MailHog (Optional but Recommended)
For testing emails locally, install and run MailHog.
```bash
~/go/bin/MailHog
```
Access the web interface at `http://localhost:8025`.
