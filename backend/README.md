# Emily Multispeciality Hospital Backend API

A FastAPI-based backend for the Emily Multispeciality Hospital AI-powered management system.

## Features

- **User Authentication**: JWT-based authentication system
- **Patient Management**: Comprehensive patient profiles and medical history
- **Doctor Management**: Healthcare professional profiles and availability
- **Appointment System**: Smart appointment scheduling and management
- **Medical Records**: Secure storage and management of medical records
- **AI Insights**: AI-powered medical analysis and recommendations
- **Database Integration**: PostgreSQL with SQLAlchemy ORM

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation
- **JWT**: Authentication tokens
- **OpenAI**: AI-powered insights
- **Supabase**: Alternative database option

## Setup Instructions

### 1. Environment Setup

Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=hospital_db
POSTGRES_PORT=5432

# Supabase Configuration (for production)
# SUPABASE_URL=your_supabase_url
# SUPABASE_ANON_KEY=your_supabase_anon_key
# SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI Configuration
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-4

# Security
SECRET_KEY=your-secret-key-change-in-production
FIRST_SUPERUSER=admin@emilyhospital.com
FIRST_SUPERUSER_PASSWORD=admin123

# CORS Origins
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"]
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Make sure PostgreSQL is running and create the database:

```bash
createdb hospital_db
```

The application will automatically create all tables on startup.

### 4. Run the Application

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## Key Endpoints

- `POST /api/v1/auth/access-token` - Login
- `POST /api/v1/auth/register` - Register new user
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/appointments/` - Get user appointments
- `POST /api/v1/appointments/` - Create appointment
- `GET /api/v1/doctors/` - Get doctors list
- `GET /api/v1/ai-insights/` - Get AI insights

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/          # API route handlers
│   │   └── api.py             # Main API router
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── security.py        # Authentication utilities
│   ├── db/
│   │   ├── base.py            # Database base configuration
│   │   ├── base_class.py      # SQLAlchemy base class
│   │   └── session.py         # Database session management
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── services/              # Business logic services
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Deployment

The application is designed to be deployed on Render.com with:

- **Frontend**: Vercel deployment
- **Backend**: Render.com deployment
- **Database**: Supabase PostgreSQL

### Render Deployment

1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.