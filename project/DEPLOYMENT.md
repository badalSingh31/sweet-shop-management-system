# Deployment Guide

This guide covers deploying the Sweet Shop Management System to production environments.

## Overview

The application consists of two parts:
- **Backend**: Python FastAPI application
- **Frontend**: React SPA built with Vite
- **Database**: Supabase (already cloud-hosted)

## Prerequisites

- [ ] GitHub/GitLab account
- [ ] Supabase project (already set up)
- [ ] Domain name (optional)
- [ ] Deployment platform accounts

## Backend Deployment Options

### Option 1: Railway (Recommended)

Railway provides easy Python deployment with automatic HTTPS.

#### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Build**
   - Railway auto-detects Python
   - Add `Procfile` in backend folder:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   - Go to project settings
   - Add variables:
   ```
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_service_key
   JWT_SECRET_KEY=random_secret_string
   ```

5. **Deploy**
   - Railway automatically deploys
   - Note your deployment URL (e.g., `https://your-app.up.railway.app`)

#### Railway Configuration

Create `railway.json` in backend folder:
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Option 2: Heroku

#### Steps:

1. Install Heroku CLI
2. Create `Procfile` in backend:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. Create `runtime.txt`:
   ```
   python-3.11.5
   ```

4. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git subtree push --prefix backend heroku main
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_KEY=your_key
   ```

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your repository
4. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Option 4: DigitalOcean App Platform

1. Create account on [DigitalOcean](https://www.digitalocean.com)
2. Create new App
3. Select repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables
6. Deploy

## Frontend Deployment Options

### Option 1: Vercel (Recommended)

Vercel is optimized for React applications.

#### Steps:

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `./` (or leave blank)
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Environment Variables**
   - Add in Vercel project settings:
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_anon_key
   ```

4. **Deploy**
   - Vercel automatically builds and deploys
   - Get URL: `https://your-app.vercel.app`

#### Vercel CLI Deployment

```bash
vercel login
vercel
vercel --prod
```

### Option 2: Netlify

1. **Deploy via Dashboard**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site"
   - Import from Git
   - Configure:
     - **Build command**: `npm run build`
     - **Publish directory**: `dist`

2. **Environment Variables**
   - Go to Site settings → Environment variables
   - Add Supabase credentials

3. **Deploy**
   - Netlify builds and deploys automatically

#### Netlify Configuration

Create `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Option 3: GitHub Pages (Static Only)

1. Update `vite.config.ts`:
```typescript
export default defineConfig({
  plugins: [react()],
  base: '/sweet-shop-management/',
})
```

2. Add to `package.json`:
```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

3. Install gh-pages:
```bash
npm install -D gh-pages
```

4. Deploy:
```bash
npm run deploy
```

### Option 4: AWS S3 + CloudFront

1. Build the app:
   ```bash
   npm run build
   ```

2. Create S3 bucket
3. Enable static website hosting
4. Upload `dist` folder
5. Configure CloudFront for HTTPS
6. Set up custom domain (optional)

## Database (Supabase)

Supabase is already cloud-hosted, but ensure:

1. **Production Settings**
   - Enable email confirmations (if needed)
   - Configure rate limiting
   - Review RLS policies
   - Enable logging

2. **Backup Strategy**
   - Enable automatic backups
   - Schedule manual backups
   - Export schema regularly

3. **Performance**
   - Review and optimize indexes
   - Monitor query performance
   - Set up connection pooling if needed

## Environment Variables

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET_KEY=generate_strong_random_string
```

### Frontend (.env)
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

## Custom Domain Setup

### Frontend (Vercel)

1. Add domain in Vercel dashboard
2. Add DNS records from your provider:
   - Type: `A`, Name: `@`, Value: `76.76.21.21`
   - Type: `CNAME`, Name: `www`, Value: `cname.vercel-dns.com`
3. Wait for DNS propagation (up to 48 hours)

### Backend (Railway)

1. Add custom domain in Railway settings
2. Add CNAME record:
   - Name: `api` (or subdomain)
   - Value: Your Railway domain
3. Enable HTTPS (automatic)

## CORS Configuration

Update backend CORS settings for production:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://www.your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Checklist

- [ ] Use HTTPS for all connections
- [ ] Enable CORS only for your frontend domain
- [ ] Use strong JWT secret keys
- [ ] Keep service role key secret
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerts
- [ ] Regular security updates
- [ ] Review and audit RLS policies
- [ ] Enable Supabase auth rate limiting
- [ ] Configure CSP headers

## Monitoring & Logging

### Backend Monitoring

1. **Railway/Heroku**
   - Built-in metrics dashboard
   - Set up log drains

2. **Custom Monitoring**
   - Sentry for error tracking
   - LogRocket for session replay
   - Datadog for APM

### Frontend Monitoring

1. **Vercel Analytics**
   - Built-in Web Vitals
   - Traffic analytics

2. **Third-party**
   - Google Analytics
   - Mixpanel
   - Amplitude

### Database Monitoring

- Supabase dashboard metrics
- Query performance monitoring
- Connection pool monitoring
- Storage usage tracking

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          # Railway CLI deploy commands

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Post-Deployment Checklist

- [ ] Test all API endpoints
- [ ] Verify authentication works
- [ ] Test CRUD operations
- [ ] Check search functionality
- [ ] Test purchase flow
- [ ] Verify admin features
- [ ] Test on mobile devices
- [ ] Check all environment variables
- [ ] Verify HTTPS works
- [ ] Test error handling
- [ ] Monitor initial traffic
- [ ] Set up alerts
- [ ] Document deployment URLs
- [ ] Update README with live links

## Rollback Plan

### Backend
```bash
# Railway
railway rollback

# Heroku
heroku rollback

# Manual
git revert HEAD
git push
```

### Frontend
```bash
# Vercel - Use dashboard to rollback to previous deployment
# Or via CLI
vercel rollback
```

## Scaling Considerations

### Backend
- Use connection pooling
- Enable caching (Redis)
- Implement rate limiting
- Use CDN for static assets
- Consider serverless functions

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- Service worker caching
- CDN distribution

### Database
- Enable read replicas
- Optimize indexes
- Use caching layer
- Monitor query performance
- Implement pagination

## Cost Optimization

### Free Tier Options
- **Frontend**: Vercel (Free tier includes)
  - 100GB bandwidth
  - Unlimited static sites
  - Automatic HTTPS

- **Backend**: Railway (Free tier includes)
  - $5 credit/month
  - 500 hours runtime

- **Database**: Supabase (Free tier includes)
  - 500MB database
  - 1GB file storage
  - 50MB file uploads
  - 2GB bandwidth

### Paid Recommendations
- Upgrade Supabase for production (~$25/month)
- Vercel Pro for analytics (~$20/month)
- Railway Pro for better resources (~$20/month)

## Support & Maintenance

### Regular Tasks
- Weekly: Review error logs
- Monthly: Check dependencies for updates
- Quarterly: Security audit
- Yearly: Performance optimization review

### Update Strategy
1. Test updates locally
2. Deploy to staging (if available)
3. Run automated tests
4. Deploy to production
5. Monitor for issues

---

## Quick Deploy Commands

### Complete Deployment
```bash
# Backend (Railway)
cd backend
railway login
railway init
railway up

# Frontend (Vercel)
cd ..
vercel login
vercel
```

## Useful Links

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Heroku Docs](https://devcenter.heroku.com)
- [Netlify Docs](https://docs.netlify.com)

---

**Need Help?** Check the troubleshooting section in README.md or open an issue on GitHub.
