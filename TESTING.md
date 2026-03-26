# Testing Guide - Golf Charity Platform

## Quick Start Test

### 1. Local Testing (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser to http://localhost:5000
```

---

## Test Scenarios

### Scenario 1: User Signup

**Steps:**
1. Go to `/signup`
2. Fill in:
   - Name: "John Golfer"
   - Email: "john@example.com"
   - Password: "testpass123"
3. Click "Sign Up"

**Expected:**
- Account created
- Redirected to dashboard
- Welcome message shows your name

**Verify:**
- Database created `golf_platform.db` in project folder
- User can access `/dashboard`

---

### Scenario 2: User Signin

**Steps:**
1. Click "Logout"
2. Go to `/signin`
3. Enter:
   - Email: "john@example.com"
   - Password: "testpass123"
4. Click "Sign In"

**Expected:**
- Signed in successfully
- Redirected to dashboard

**Fail Test:**
- Try wrong password
- Should see "Invalid credentials" error

---

### Scenario 3: Add Golf Score

**Steps:**
1. On dashboard, scroll to "Add New Score" section
2. Enter:
   - Score: 32
   - Date: Today's date
3. Click "Add Score"

**Expected:**
- Success message shows
- Page refreshes
- Score appears in "Your Scores (Last 5)" table

**Validation:**
- Try score = 0 (should fail)
- Try score = 50 (should fail)
- Try score = 25 (should succeed)
- Try duplicate date (should fail with "already exists" error)

---

### Scenario 4: Score History

**Steps:**
1. Add 5+ different scores on different dates
2. On dashboard, check "Your Scores (Last 5)" table

**Expected:**
- Only last 5 scores shown
- Ordered by date (newest first)
- All scores are 1-45 range

---

### Scenario 5: Session Persistence

**Steps:**
1. Sign in
2. Add a score
3. Close browser completely
4. Reopen and go to localhost:5000

**Expected:**
- Redirected to dashboard (still logged in via session)
- Score is still there

**Verify:**
- Session cookie is set
- Can work offline briefly (app is local)

---

### Scenario 6: Subscription Toggle

**Steps:**
1. On dashboard, see subscription status box
2. Click "Subscribe Now" button

**Expected:**
- Button disappears
- Status changes to "Active"
- Page shows "Your subscription is active!"

---

### Scenario 7: Access Control

**Test unauthorized access:**

1. Open browser console (F12)
2. Clear cookies via:
   ```javascript
   document.cookie.split(';').forEach(c => 
     document.cookie = c.replace(/^ +/, '')
       .replace(/=.*/, '=;expires=' + new Date().toUTCString())
   );
   ```
3. Go to `/dashboard`

**Expected:**
- Redirected to `/signin`
- Cannot access protected routes without login

---

### Scenario 8: API Direct Testing

Use curl or Postman to test endpoints:

**Get User Info:**
```bash
curl -H "Cookie: session=YOUR_SESSION_ID" \
  http://localhost:5000/api/user
```

**Add Score (requires session):**
```bash
curl -X POST http://localhost:5000/api/score \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_ID" \
  -d '{"score": 28, "date": "2024-01-15"}'
```

**Get Draws:**
```bash
curl http://localhost:5000/api/draws
```

---

## Performance Testing

### Load Time Test

1. Open DevTools (F12)
2. Go to Network tab
3. Reload page (`Ctrl+R`)

**Expected:**
- Page loads in < 2 seconds
- Database initialization takes < 1 second

### Database Growth Test

1. Add 100+ scores rapidly
2. Check file size of `golf_platform.db`

**Expected:**
- File remains small (< 1 MB for 1000 scores)
- Queries still fast

---

## Mobile Responsive Test

### Test on Mobile Sizes

```bash
# In Chrome DevTools (F12)
1. Click device toolbar icon (phone/tablet)
2. Test different sizes:
   - iPhone (375px)
   - iPad (768px)
   - Large desktop (1920px)
```

**Check:**
- Navigation bar responsive
- Forms stack on mobile
- Stats boxes stack on mobile
- Text readable on all sizes

---

## Error Handling Test

### Test Various Error Scenarios

| Scenario | Test | Expected |
|----------|------|----------|
| Empty email | Signup with no email | Error message |
| Empty password | Signin with no password | Error message |
| Invalid score (0) | Add score 0 | "Score must be 1-45" |
| Invalid score (100) | Add score 100 | "Score must be 1-45" |
| Duplicate email | Signup with same email | "Email already exists" |
| Future date score | Add score for future date | Accept (no validation) |
| Missing required field | POST to API without data | Error response |
| Unauthorized API call | Call `/api/user` without session | 401 error |
| Not found | Visit `/nonexistent` | 404 page |

---

## Database Inspection

### View Database Contents

```bash
# List all users
sqlite3 golf_platform.db "SELECT * FROM users;"

# List all scores
sqlite3 golf_platform.db "SELECT * FROM scores;"

# Count records
sqlite3 golf_platform.db "SELECT COUNT(*) FROM users;"

# View schema
sqlite3 golf_platform.db ".schema"
```

---

## Automated Testing Script

Create `test_app.py`:

```python
import requests
import json

BASE_URL = 'http://localhost:5000'
session = requests.Session()

def test_signup():
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass'
    }
    response = session.post(f'{BASE_URL}/signup', json=data)
    assert response.status_code == 200
    print("✓ Signup test passed")

def test_signin():
    data = {
        'email': 'test@example.com',
        'password': 'testpass'
    }
    response = session.post(f'{BASE_URL}/signin', json=data)
    assert response.status_code == 200
    print("✓ Signin test passed")

def test_add_score():
    data = {
        'score': 35,
        'date': '2024-01-15'
    }
    response = session.post(f'{BASE_URL}/api/score', json=data)
    assert response.status_code == 200
    print("✓ Add score test passed")

def test_get_user():
    response = session.get(f'{BASE_URL}/api/user')
    assert response.status_code == 200
    print("✓ Get user test passed")

if __name__ == '__main__':
    test_signup()
    test_signin()
    test_add_score()
    test_get_user()
    print("\nAll tests passed!")
```

Run it:
```bash
python test_app.py
```

---

## Browser Console Testing

Open DevTools (F12), Console tab:

```javascript
// Check local storage
console.log(localStorage);

// Check session
fetch('/api/user').then(r => r.json()).then(console.log);

// Test score submission
fetch('/api/score', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({score: 30, date: '2024-01-20'})
}).then(r => r.json()).then(console.log);
```

---

## Known Issues to Test

These should work correctly:

- ✓ Can signup, signin, logout
- ✓ Scores validate (1-45)
- ✓ Cannot add duplicate score on same date
- ✓ Dashboard shows last 5 scores
- ✓ Subscription toggle works
- ✓ Responsive on mobile
- ✓ Session persists across page reloads
- ✓ 404 page shows for invalid routes

---

## Pre-Deployment Checklist

Before deploying to Vercel:

- [ ] Test all 8 scenarios above locally
- [ ] No console errors (F12)
- [ ] Database file created (`golf_platform.db`)
- [ ] Can signup with real email
- [ ] Can add multiple scores
- [ ] Dashboard loads fast
- [ ] Mobile responsive works
- [ ] Session persists
- [ ] No hardcoded secrets in code
- [ ] `.env` not committed to git

---

## Tips

**Clear data between tests:**
```bash
# Delete database to start fresh
rm golf_platform.db
python app.py  # Recreates empty DB
```

**Check running processes:**
```bash
# See if app is running
lsof -i :5000
# or on Windows
netstat -ano | findstr :5000
```

**View app logs:**
```bash
# Run with debug output
python -u app.py
```

---

## Success Criteria

If all scenarios pass, your app is ready:

✓ Users can signup and signin  
✓ Scores are tracked correctly  
✓ Data persists in database  
✓ UI is responsive  
✓ No errors in logs  
✓ Session management works  
✓ API endpoints respond correctly  

**Status: Ready for Vercel deployment!**
