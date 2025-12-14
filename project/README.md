# Sweet Shop Management System

A comprehensive full-stack web application for managing a sweet shop with inventory tracking, user authentication, role-based access control, and purchase management.

![Sweet Shop Banner](https://images.pexels.com/photos/65882/chocolate-dark-coffee-confiserie-65882.jpeg?auto=compress&cs=tinysrgb&w=1200)

## 🍬 Features

### Core Functionality
- **User Authentication**: Secure registration and login system using Supabase Auth
- **Role-Based Access Control**: Separate permissions for regular users and administrators
- **Inventory Management**: Full CRUD operations for sweet products (Admin only)
- **Purchase System**: Users can purchase sweets with automatic stock updates
- **Restock Management**: Administrators can restock inventory
- **Advanced Search & Filtering**: Search by name, category, and price range
- **Real-time Updates**: Live inventory synchronization
- **Responsive Design**: Beautiful, mobile-friendly interface

### User Features
- Register and login securely
- Browse available sweets with detailed information
- Search and filter sweets by multiple criteria
- Purchase sweets with quantity selection
- View real-time stock availability
- See total purchase price calculations

### Admin Features
- Add new sweets to inventory
- Update existing sweet information
- Delete sweets from inventory
- Restock inventory quantities
- Access to all user features

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icon library
- **Supabase Client** - Database and authentication

### Backend
- **Python FastAPI** - High-performance web framework
- **Supabase** - PostgreSQL database with built-in auth
- **Pydantic** - Data validation
- **JWT** - Token-based authentication

### Testing
- **pytest** - Python testing framework
- **pytest-asyncio** - Async testing support
- **pytest-cov** - Code coverage reporting

### Database
- **PostgreSQL** (via Supabase)
- **Row Level Security (RLS)** for data protection
- **Automated triggers** for timestamps and profiles

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd sweet-shop-management
```

### 2. Database Setup

The database is already configured in Supabase with the following schema:
- `profiles` - User profile information with roles
- `sweets` - Sweet inventory data
- `purchases` - Purchase transaction history

All tables have Row Level Security (RLS) enabled for data protection.

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `backend/.env` and add your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
JWT_SECRET_KEY=your_jwt_secret
```

### 4. Frontend Setup

```bash
cd ..  # Back to root directory

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🏃 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Start Frontend (Terminal 2)

```bash
npm run dev
```

Frontend will run at: http://localhost:5173

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest

# With coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # On Mac
# or
start htmlcov/index.html  # On Windows
```

### Test Results Summary
- Authentication tests: ✅ All passing
- Sweets CRUD tests: ✅ All passing
- Purchase system tests: ✅ All passing
- Search & filter tests: ✅ All passing
- Role-based access tests: ✅ All passing

## 📁 Project Structure

```
sweet-shop-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Supabase client
│   │   ├── models.py            # Pydantic models
│   │   ├── auth.py              # Authentication utilities
│   │   └── routers/
│   │       ├── auth.py          # Auth endpoints
│   │       └── sweets.py        # Sweets endpoints
│   ├── tests/
│   │   ├── conftest.py          # Test configuration
│   │   ├── test_auth.py         # Auth tests
│   │   └── test_sweets.py       # Sweets tests
│   ├── requirements.txt
│   ├── pytest.ini
│   └── README.md
├── src/
│   ├── components/
│   │   ├── AddSweetModal.tsx    # Admin add sweet form
│   │   ├── AuthForm.tsx         # Login/Register form
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── Header.tsx           # Navigation header
│   │   ├── ProtectedRoute.tsx   # Route guard
│   │   ├── SearchFilters.tsx    # Search & filter UI
│   │   └── SweetCard.tsx        # Sweet product card
│   ├── contexts/
│   │   └── AuthContext.tsx      # Auth state management
│   ├── lib/
│   │   └── supabase.ts          # Supabase client
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }
  ```

- `POST /api/auth/login` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### Sweets (Protected Routes)
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/search?name=chocolate&category=chocolate&min_price=1.0&max_price=5.0` - Search sweets
- `POST /api/sweets` - Create sweet (Admin only)
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory (Protected Routes)
- `POST /api/sweets/{id}/purchase` - Purchase sweet
  ```json
  {
    "quantity": 2
  }
  ```

- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)
  ```json
  {
    "quantity": 50
  }
  ```

## 👥 User Roles & Permissions

### Regular User
- ✅ View all sweets
- ✅ Search and filter sweets
- ✅ Purchase sweets
- ❌ Add/Edit/Delete sweets
- ❌ Restock inventory

### Administrator
- ✅ All user permissions
- ✅ Add new sweets
- ✅ Edit existing sweets
- ✅ Delete sweets
- ✅ Restock inventory

### Creating an Admin User

To create an admin user, you need to manually update the role in the database:

1. Register a normal user through the app
2. Go to your Supabase dashboard
3. Navigate to Table Editor → profiles
4. Find the user and change their `role` from `'user'` to `'admin'`
5. Logout and login again to see admin features

## 🎨 Design Philosophy

The application features a warm, inviting design inspired by candy stores:
- **Color Palette**: Orange and pink gradients for a sweet, friendly feel
- **Typography**: Bold headings with clear hierarchy
- **Layout**: Card-based design with generous spacing
- **Responsiveness**: Mobile-first approach with breakpoints for all screen sizes
- **Animations**: Subtle transitions and hover effects for better UX
- **Accessibility**: High contrast ratios and clear visual feedback

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Secure password storage via Supabase Auth
- **Row Level Security**: Database-level access control
- **Role-Based Access**: Frontend and backend permission checks
- **Input Validation**: Pydantic validation on backend
- **CORS Protection**: Configured CORS policies
- **SQL Injection Protection**: Parameterized queries via Supabase client

## 🧠 My AI Usage

### AI Tools Used
I used **Claude (Anthropic)** as my primary AI assistant throughout this project development.

### How I Used AI

#### 1. Project Architecture & Planning
- **Usage**: Asked Claude to help design the overall architecture and tech stack selection
- **Value**: Got recommendations for FastAPI + React + Supabase combination based on project requirements
- **Human Input**: Made final decisions on specific versions and libraries

#### 2. Database Schema Design
- **Usage**: Collaborated with Claude on designing the PostgreSQL schema with proper relationships
- **Value**: Got suggestions for RLS policies, indexes, and triggers
- **Human Input**: Reviewed and adjusted policies for security requirements, added sample data

#### 3. Backend API Development
- **Usage**: Claude helped generate boilerplate code for FastAPI routes, models, and auth utilities
- **Value**: Saved significant time on repetitive code structure
- **Human Input**: Customized error handling, validation logic, and added business logic

#### 4. Test Suite Creation
- **Usage**: AI assisted in writing pytest test cases covering various scenarios
- **Value**: Comprehensive test coverage with edge cases I might have missed
- **Human Input**: Added specific test cases for business requirements and verified all tests pass

#### 5. Frontend Component Structure
- **Usage**: Claude helped scaffold React components with TypeScript
- **Value**: Consistent component patterns and proper type definitions
- **Human Input**: Implemented specific UI/UX requirements, responsive design, and animations

#### 6. UI/UX Design
- **Usage**: Asked for suggestions on color schemes, layout patterns, and user flows
- **Value**: Got ideas for the orange/pink gradient theme and card-based layout
- **Human Input**: Made all final design decisions, implemented custom animations, and ensured brand consistency

#### 7. Error Handling & Edge Cases
- **Usage**: Claude helped identify potential error scenarios
- **Value**: More robust error handling and user feedback
- **Human Input**: Implemented user-friendly error messages and recovery flows

#### 8. Documentation
- **Usage**: AI assisted in writing comprehensive README and inline code documentation
- **Value**: Well-structured documentation with examples
- **Human Input**: Added personal insights, setup instructions, and troubleshooting tips

### Impact on Development Workflow

**Positive Impacts:**
- ⚡ **Speed**: Reduced development time by ~40% through rapid prototyping
- 🧪 **Quality**: More comprehensive test coverage
- 📚 **Learning**: Discovered new patterns and best practices
- 🎨 **Creativity**: Got design inspiration I wouldn't have thought of alone

**Challenges:**
- 🔍 **Code Review**: Had to carefully review all AI-generated code
- 🎯 **Context**: Sometimes needed to provide detailed context for specific requirements
- 🐛 **Debugging**: AI-generated code occasionally had subtle bugs requiring fixes

### Reflection

Using AI as a development partner was transformative. Rather than replacing my skills, it amplified them by:
1. Handling repetitive boilerplate code
2. Suggesting best practices and patterns
3. Catching edge cases in testing
4. Accelerating the documentation process

However, **human judgment remained critical** for:
- Architecture decisions
- Security considerations
- User experience design
- Business logic implementation
- Code quality assurance

The key to effective AI usage was treating it as a **junior developer** - great at implementation, but requiring oversight and direction. I always reviewed, tested, and understood every piece of code before committing.

## 📸 Screenshots

### Login/Register Page
Beautiful authentication interface with gradient background and smooth transitions.

### Dashboard
Main view showing all sweets with search and filter capabilities.

### Admin Features
Add new sweets modal with comprehensive form validation.

### Purchase Flow
Intuitive purchase modal with quantity selection and price calculation.

## 🚀 Deployment

### Backend Deployment (Heroku/Railway/Render)

1. Add a `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Ensure `requirements.txt` is up to date

3. Set environment variables in your hosting platform

### Frontend Deployment (Vercel/Netlify)

1. Build the frontend:
```bash
npm run build
```

2. Deploy the `dist` folder

3. Set environment variables in deployment settings

## 🤝 Contributing

This project was developed as part of a TDD kata assessment. For contributing guidelines, please reach out.

## 📝 License

MIT License - feel free to use this project for learning purposes.

## 🐛 Known Issues & Future Enhancements

### Current Limitations
- No purchase history view for users
- Image uploads not implemented (URL input only)
- No password reset functionality
- No email verification

### Planned Features
- 📊 Analytics dashboard for admins
- 📧 Email notifications for purchases
- 🖼️ Image upload and storage
- 🎫 Discount codes and promotions
- 📱 Progressive Web App (PWA) support
- 🌐 Multi-language support
- 📈 Sales reports and charts
- 💳 Payment gateway integration

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team.

## 🙏 Acknowledgments

- Supabase for the excellent backend-as-a-service platform
- FastAPI for the high-performance Python framework
- React and Vite teams for the modern frontend tooling
- Pexels for the beautiful stock images
- The open-source community for inspiration and tools

---
-login page (https://drive.google.com/file/d/1atMSxKDjM-1v5UvNP1C7dlAzrr0c2iDV/view?usp=sharing)
**Built with ❤️ and 🍬 using Test-Driven Development**

*Note: This project demonstrates modern full-stack development practices including TDD, clean code principles, security best practices, and effective AI collaboration.*
