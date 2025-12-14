# Sweet Shop Management System - Backend

A robust Python FastAPI backend for managing a sweet shop with inventory, authentication, and purchase tracking.

## Features

- JWT-based authentication with Supabase
- RESTful API endpoints
- Role-based access control (Admin/User)
- Comprehensive test coverage
- Database integration with Supabase PostgreSQL

## Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Testing**: pytest, pytest-cov
- **Validation**: Pydantic

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Add your Supabase credentials to `.env`:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

## Running the Server

Development mode with auto-reload:
```bash
uvicorn app.main:app --reload --port 8000
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Sweets (Protected)
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/search` - Search sweets
- `POST /api/sweets` - Create sweet (Admin only)
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory (Protected)
- `POST /api/sweets/{id}/purchase` - Purchase sweet
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration management
│   ├── database.py       # Supabase client setup
│   ├── models.py         # Pydantic models
│   ├── auth.py          # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints
│       └── sweets.py     # Sweets endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures
│   ├── test_auth.py      # Auth tests
│   └── test_sweets.py    # Sweets tests
├── requirements.txt
├── pytest.ini
└── README.md
```

## Development

This project follows Test-Driven Development (TDD) principles. Before implementing new features:

1. Write failing tests first
2. Implement the minimum code to pass tests
3. Refactor while keeping tests green

## License

MIT
