# Golf Charity Subscription Platform

A minimal, deployable golf scoring and charity fundraising platform built with Flask and HTML.

## Features

- ⛳ **Score Tracking**: Record Stableford scores (1-45 points) from golf rounds
- 🎰 **Monthly Draws**: Qualified scores enter monthly draws with tiered prizes
- ❤️ **Charity Support**: 10% of subscriptions go to player-chosen charities
- 📊 **Simple Dashboard**: View scores, subscription status, and draw info
- 🔐 **User Authentication**: Secure signup and signin

## Tech Stack

- **Backend**: Flask (Python) with SQLite database
- **Frontend**: HTML + CSS (no JavaScript frameworks)
- **Deployment**: Vercel (serverless)

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   cd golf-platform
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000`

3. **Create a user**:
   - Go to `/signup` and create an account
   - Add some golf scores from the dashboard
   - Subscribe to activate draw eligibility

### Environment Variables

Create a `.env` file (or use `.env.example`):
```
SECRET_KEY=your-secret-key
FLASK_ENV=production
DATABASE_URL=golf_platform.db
```

## API Endpoints

### Authentication
- `POST /signup` - Create new account
- `POST /signin` - Sign in with email/password
- `GET /logout` - Sign out

### Dashboard
- `GET /dashboard` - User dashboard with scores

### Scoring
- `POST /api/score` - Add a new golf score
- `GET /api/draws` - Get recent completed draws

### Subscription
- `POST /api/subscribe` - Activate subscription

## Database Schema

- **users**: Email, name, password, subscription status, charity contribution %
- **scores**: User scores with dates (keeps last 5)
- **draws**: Monthly draws with winning numbers
- **winners**: Draw winners with prize amounts

## Deployment to Vercel

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your GitHub repository
   - Vercel will auto-detect Flask setup
   - Add environment variables in Settings → Environment Variables
   - Deploy!

3. **Set production SECRET_KEY**:
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add `SECRET_KEY` with a secure random string

## Subscription Plans

| Plan | Price | Features |
|------|-------|----------|
| Monthly | $9.99 | Unlimited scores, monthly draws, charity support |
| Yearly | $99.99 | Same features, best value (12 months) |

## Draw Structure

Your top 5 scores qualify for monthly draws.

**Prize Distribution**:
- 5-number match: 40% of pool
- 4-number match: 35% of pool
- 3-number match: 25% of pool

## File Structure

```
golf-platform/
├── app.py                 # Flask application
├── wsgi.py               # WSGI entry point for Vercel
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── .env.example         # Example environment variables
├── golf_platform.db     # SQLite database (auto-created)
├── templates/
│   ├── base.html        # Base template with navbar
│   ├── index.html       # Homepage
│   ├── auth.html        # Signup/Signin forms
│   ├── dashboard.html   # User dashboard
│   └── 404.html         # Error page
└── static/              # Static files (CSS, JS)
```

## Notes

- This is a **minimum viable product (MVP)** - bare minimum complexity for rapid deployment
- Database is SQLite (perfect for Vercel's serverless environment)
- No external API keys required (Stripe integration removed for simplicity)
- Styling is pure CSS (no Tailwind or frameworks)
- User passwords stored plaintext (use bcrypt in production!)

## Future Enhancements

If you want to expand:
- Add password hashing with bcrypt
- Integrate Stripe for real payments
- Add actual draw generation logic
- Create admin dashboard for draw management
- Add email notifications

## Support

For issues or questions, check the code comments or reach out to the development team.

---

**Deploy with Vercel**: One-click deployment to production with automatic builds and previews.
