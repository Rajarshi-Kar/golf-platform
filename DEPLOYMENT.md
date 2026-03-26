# Deployment Guide - Golf Charity Platform

Deploy your Flask app to Vercel in 5 minutes.

## Prerequisites

- GitHub account (app code)
- Vercel account (free at vercel.com)
- Git installed

## Step 1: Prepare Your Repository

```bash
# If not already done:
cd golf-platform
git init
git add .
git commit -m "Initial commit: Golf Charity Platform MVP"
```

## Step 2: Push to GitHub

1. Create a new repository on GitHub (don't initialize with README)
2. Push your code:

```bash
git remote add origin https://github.com/yourusername/golf-platform.git
git branch -M main
git push -u origin main
```

## Step 3: Connect to Vercel

### Option A: Via GitHub (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Select "Import Git Repository"
4. Find and click "golf-platform"
5. Select "Python" framework preset (or let it auto-detect)
6. Configure project settings:
   - **Project Name**: golf-platform
   - **Root Directory**: ./ (current)
   - **Framework Preset**: Flask
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: (leave blank)
   - **Environment Variables**: Add these (see below)

### Option B: Via Vercel CLI

```bash
npm i -g vercel        # Install Vercel CLI
vercel                 # Follow prompts to create project
vercel env add SECRET_KEY    # Add environment variable
# Enter a secure random string when prompted
vercel deploy          # Deploy
```

## Step 4: Add Environment Variables

In Vercel Dashboard:

1. Go to Settings → Environment Variables
2. Add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate a random string (use `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `FLASK_ENV` | `production` |

3. Redeploy for variables to take effect

## Step 5: Database Persistence

⚠️ **Important**: SQLite databases don't persist on Vercel because:
- Vercel has serverless, ephemeral storage
- Each deployment creates a fresh filesystem
- Databases should be cloud-based for production

### For MVP (Testing Only):
- Database in this setup is local SQLite - useful for development
- Deployment will work, but database resets on each redeploy
- Good enough for testing/demo

### For Production:
Consider migrating to cloud database:

**Option 1: PostgreSQL (Recommended)**
```python
import psycopg2
# Replace SQLite with PostgreSQL connection
```

**Option 2: MongoDB**
```python
from pymongo import MongoClient
# Use MongoDB Atlas (free tier available)
```

**Option 3: Firebase**
```python
import firebase_admin
# Real-time database with free tier
```

## Step 6: Deploy!

### First Deployment
1. Vercel auto-deploys from GitHub on every push
2. Wait for build to complete (usually 1-2 minutes)
3. Check build logs if there are issues
4. View your app at: `https://golf-platform.vercel.app`

### Subsequent Deployments
Just push to GitHub:
```bash
git add .
git commit -m "Update description"
git push origin main
```

Vercel automatically redeploys!

## Testing Your Deployment

1. Visit your Vercel URL
2. Test signup/signin workflow
3. Add a test score
4. Check database persists (note: will reset on next deploy with SQLite)

## Troubleshooting

### Build Failed
- Check build logs in Vercel dashboard
- Common issues:
  - Missing `requirements.txt`
  - Missing environment variables
  - Syntax errors in Python

**Fix**: Push a new commit:
```bash
git add .
git commit -m "Fix build error"
git push
```

### Import Errors
- Ensure all imports are in `requirements.txt`
- Example: Add `flask==3.0.0` if Flask import fails

### 502 Bad Gateway
- App crashed at runtime
- Check Vercel logs: Settings → Function Logs
- Ensure `FLASK_ENV=production`

### Database Not Persisting
- This is expected with SQLite on Vercel
- Consider migrating to cloud database (see above)

## Custom Domain (Optional)

1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain (e.g., `golfl.club`)
3. Follow DNS setup instructions
4. SSL certificate auto-enabled

## Performance Optimization

- Vercel's serverless functions have cold start times (~500ms)
- First request after deployment may be slow
- Subsequent requests are fast
- Use Vercel Analytics to monitor performance

## Cost

**Free Tier Includes**:
- 100 deployments/day
- Serverless functions
- SSL/HTTPS
- Edge network (CDN)
- Custom domains

**Paid Plans** ($20+/month):
- No deployment limits
- Priority support
- Backend usage overages charged

For this MVP, free tier is plenty!

## Next Steps

1. **Setup complete** ✓
2. **Database migration** (optional, for production)
3. **Add payment processing** (when ready)
4. **Email notifications** (when ready)
5. **Admin dashboard** (when ready)

## Security Checklist

- [ ] SECRET_KEY is long and random (32+ characters)
- [ ] Never commit `.env` file to GitHub
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (automatic with Vercel)
- [ ] Keep dependencies updated: `pip list --outdated`

## Monitoring & Logs

In Vercel Dashboard:
- **Deployments**: See build history
- **Function Logs**: Real-time app logs
- **Analytics**: Usage statistics
- **Error Tracking**: Caught errors

Set up alerts for failed builds:
Settings → Alerts → Create Alert

## Rolling Back

If deployment breaks:
1. Go to Deployments tab
2. Find a previous working deployment
3. Click "●●●" menu → "Promote to Production"
4. Done! Instantly reverted.

## Support

- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
- GitHub Support: https://github.com/support

---

**🚀 Your app is now deployed and live on the internet!**

Share your URL with the world. Example: `https://golf-platform-abc123.vercel.app`
