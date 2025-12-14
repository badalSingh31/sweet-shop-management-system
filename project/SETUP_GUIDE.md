# Quick Setup Guide

This guide will help you get the Sweet Shop Management System up and running quickly.

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.9+ installed
- [ ] Supabase account created
- [ ] Git installed

## Step-by-Step Setup

### 1. Get Supabase Credentials

1. Go to [supabase.com](https://supabase.com) and sign in
2. Create a new project or select existing one
3. Go to Project Settings → API
4. Copy:
   - Project URL (looks like: `https://xxxxx.supabase.co`)
   - anon/public key (starts with `eyJ...`)
   - service_role key (starts with `eyJ...`)

### 2. Database Setup

The database schema is already set up via migrations. The system includes:
- User profiles with role management
- Sweets inventory table
- Purchase tracking table
- Sample sweet products

### 3. Backend Configuration

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `backend/.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET_KEY=any-random-string-here
```

### 4. Frontend Configuration

```bash
# From project root
npm install

# Create .env file
cp .env.example .env
```

Edit `.env`:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### 6. Create Your First Admin User

1. Open http://localhost:5173
2. Click "Register" and create an account
3. Go to your Supabase Dashboard
4. Navigate to: Table Editor → profiles
5. Find your user and change `role` from `user` to `admin`
6. Logout and login again
7. You'll now see the "Add Sweet" button and admin features

## Testing the Application

### Test Regular User Features
1. Register a new account
2. Browse sweets on the dashboard
3. Use search and filters
4. Purchase a sweet (quantity will decrease)

### Test Admin Features
1. Login with admin account
2. Click "Add Sweet" to create new products
3. Use the edit button on sweet cards
4. Restock inventory using the package icon
5. Delete sweets using the trash icon

## Common Issues

### Backend Won't Start
- Make sure virtual environment is activated
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check .env file has correct Supabase credentials

### Frontend Won't Connect
- Verify .env file exists and has correct values
- Make sure environment variables start with `VITE_`
- Try clearing browser cache and restarting dev server

### Can't Login
- Check Supabase dashboard to verify user was created
- Make sure email confirmation is disabled in Supabase Auth settings
- Verify backend is running and accessible

### Images Not Showing
- Images use Pexels URLs by default
- Make sure URLs are valid and accessible
- You can update image URLs when editing sweets

## Next Steps

1. Explore the API documentation: http://localhost:8000/docs
2. Run the test suite: `cd backend && pytest`
3. Customize the design to match your brand
4. Deploy to production (see README.md for deployment guide)

## Support

If you encounter issues:
1. Check the main README.md for detailed documentation
2. Review error messages in browser console and terminal
3. Verify all environment variables are set correctly
4. Make sure Supabase project is active and accessible

## Demo Credentials (After Setup)

Create these accounts for testing:

**Admin Account:**
- Email: admin@sweetshop.com
- Password: admin123456
- Set role to 'admin' in Supabase

**Test User:**
- Email: user@sweetshop.com
- Password: user123456
- Keep role as 'user'

---

**Happy Coding! 🍬**
