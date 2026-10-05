# AI Government Platform

AI Government Platform is a full-stack complaint and grievance redressal system. Citizens can register, submit complaints, track complaint status, and use a chatbot. Staff can manage assigned complaints, while admins can register staff, review analytics, configure settings, and manually assign work.

## Features

- Citizen registration, login, password reset, complaint submission, and complaint tracking
- Staff/admin JWT authentication with role-based route protection
- AI department prediction for complaint routing
- Priority prediction and severity scoring
- Rule-based fallback routing when model confidence is low
- Staff workload-aware assignment
- Admin dashboards for complaints, staff, reports, and settings
- Multilingual frontend support through a React language context
- Chatbot guidance for complaint-related questions

## Tech Stack

Frontend:
- React 18
- Vite
- React Router
- Tailwind CSS
- Axios
- Lucide React icons

Backend:
- Python
- Flask
- Flask-CORS
- MongoDB with PyMongo
- JWT authentication
- bcrypt / Werkzeug password hashing
- scikit-learn, pandas, NumPy, joblib for AI models
- python-dotenv for environment configuration

Development tools:
- npm
- pip / virtualenv
- Git
- MongoDB Community Server or MongoDB Atlas

## Project Structure

```text
ai_gov_platform/
|-- backend/
|   |-- ai/                  # datasets, model training, model prediction
|   |-- chatbot/             # chatbot intent and response flow
|   |-- middleware/          # JWT route middleware
|   |-- routes/              # Flask API blueprints
|   |-- services/            # assignment, routing, email, chatbot services
|   |-- utils/               # auth, security, language, ID, routing helpers
|   |-- app.py               # Flask app entry point
|   |-- db.py                # MongoDB connection
|   |-- requirements.txt     # Python dependencies
|   `-- .env.example         # backend environment template
|-- frontend/
|   |-- src/
|   |   |-- components/      # shared UI and route guards
|   |   |-- context/         # language context and hooks
|   |   |-- i18n/            # translation strings
|   |   |-- pages/           # app screens
|   |   |-- services/        # API clients
|   |   `-- utils/           # auth/session helpers
|   |-- package.json         # frontend dependencies and scripts
|   |-- vite.config.js
|   `-- .env.example         # frontend environment template
|-- .gitignore
`-- README.md
```

## Prerequisites

Install these before running the project:

- Node.js 18 or newer
- Python 3.10 or newer
- MongoDB running locally, or a MongoDB Atlas connection string
- Git

## Backend Setup

Open a terminal from the repository root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

Update `backend/.env` if needed:

```env
SECRET_KEY=replace_with_a_long_random_secret
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=ai_gov
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RESET_PASSWORD_BASE_URL=http://localhost:5173/reset-password
```

The backend runs at:

```text
http://127.0.0.1:5000
```

Health check:

```bash
curl http://127.0.0.1:5000/
```

## Frontend Setup

Open a second terminal from the repository root:

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

On macOS/Linux, create the env file with:

```bash
cp .env.example .env
```

Default frontend environment:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

The frontend runs at:

```text
http://localhost:5173
```

## How To Use

1. Start MongoDB.
2. Start the Flask backend from `backend/`.
3. Start the Vite frontend from `frontend/`.
4. Open `http://localhost:5173`.
5. Register as a citizen, submit a complaint, and save the generated complaint ID.
6. Use Track Complaint to view status updates.
7. Create an admin through `POST /api/admin/register` or by running the helper script if you choose to seed local data.
8. Login as admin to register staff, assign complaints, and view reports.
9. Login as staff to view and update assigned complaint status.

## Useful Commands

Backend:

```bash
cd backend
python app.py
python create_admin.py
python seed_staff_and_assign.py
python -m unittest discover
```

Frontend:

```bash
cd frontend
npm run dev
npm run build
npm run lint
npm run preview
```

## API Overview

Common backend routes:

- `GET /` - backend health response
- `POST /api/login` - staff/admin login
- `POST /api/admin/register` - create admin
- `POST /api/staff/register` - admin-only staff creation
- `POST /api/auth/citizen/register` - citizen registration
- `POST /api/auth/citizen/login` - citizen login
- `POST /api/complaints` - submit complaint
- `GET /api/complaints` - list complaints for authorized users
- `GET /api/complaints/<id>` - track complaint details
- `POST /api/chatbot` - chatbot response

## AI Components

The backend includes trained model artifacts and datasets in `backend/ai/`:

- Department routing model files such as `model.pkl`, `tfidf.pkl`, and label/vectorizer artifacts
- Priority model files such as `priority_model.pkl`
- Training scripts for department, priority, and semantic routing experiments
- CSV datasets for complaint and priority training

Runtime routing combines model prediction, severity scoring, language handling, keyword fallback, and workload-aware assignment.

## Security Notes

- Never commit `.env` files or real credentials.
- Use a long random `SECRET_KEY` outside development.
- Rotate any email app password or credential that was previously stored in a local `.env`.
- For production, use HTTPS, strict CORS origins, secure cookie/session policies, and a managed secrets store.

## Cleanup Notes

Generated and duplicate files are intentionally excluded:

- Python caches: `__pycache__/`, `*.pyc`
- Python virtual environments: `.venv/`, `backend/venv/`
- Node dependencies: `node_modules/`, `frontend/node_modules/`
- Frontend build outputs: `dist/`, `frontend/dist/`
- Local env files: `.env`, `.env.*` except `.env.example`

The project keeps helper and verification scripts under `backend/` because they are useful for setup, seeding, and manual checks.
