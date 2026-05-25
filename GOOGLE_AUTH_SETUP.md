# 🔐 Google Authentication Setup Guide

## Overview

I've added Google OAuth 2.0 authentication to your platform! Users can now sign in with their Google accounts.

## ✅ What's Been Implemented

### Backend Changes:
1. ✅ Added Google OAuth fields to User model (`google_id`, `oauth_provider`, `profile_picture`)
2. ✅ Created database migration (004_add_google_oauth.py)
3. ✅ Added `authlib` dependency for OAuth
4. ✅ Created Google OAuth endpoints:
   - `GET /api/v1/auth/google/login` - Initiates Google login
   - `GET /api/v1/auth/google/callback` - Handles Google callback
5. ✅ Updated config to support Google OAuth settings

### What You Need to Do:

## 📋 Step 1: Create Google OAuth Credentials

### 1.1 Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 1.2 Create a New Project (or select existing)
1. Click "Select a project" at the top
2. Click "NEW PROJECT"
3. Name it: "Oil & Gas Valuation Platform"
4. Click "CREATE"

### 1.3 Enable Google+ API
1. Go to "APIs & Services" > "Library"
2. Search for "Google+ API"
3. Click "ENABLE"

### 1.4 Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **Oil & Gas Valuation Platform**
   - User support email: **your-email@gmail.com**
   - Developer contact: **your-email@gmail.com**
   - Click "SAVE AND CONTINUE"
   - Scopes: Click "ADD OR REMOVE SCOPES"
     - Select: `userinfo.email`, `userinfo.profile`, `openid`
   - Click "SAVE AND CONTINUE"
   - Test users: Add your email
   - Click "SAVE AND CONTINUE"

4. Back to Credentials:
   - Application type: **Web application**
   - Name: **Oil & Gas Valuation Platform**
   - Authorized JavaScript origins:
     ```
     http://localhost:5173
     http://localhost:3000
     ```
   - Authorized redirect URIs:
     ```
     http://localhost:8000/api/v1/auth/google/callback
     ```
   - Click "CREATE"

5. **IMPORTANT**: Copy your credentials:
   - Client ID: `xxxxx.apps.googleusercontent.com`
   - Client Secret: `xxxxx`

## 📋 Step 2: Update Environment Variables

### 2.1 Update `.env` file in backend folder

Create or update `/Users/saketsmac/Desktop/Finanace Project/backend/.env`:

```bash
# Existing variables...
DATABASE_URL=postgresql://user:password@postgres:5432/valuation_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here

# Add these Google OAuth variables:
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
FRONTEND_URL=http://localhost:5173
```

**Replace**:
- `your-client-id-here` with your actual Google Client ID
- `your-client-secret-here` with your actual Google Client Secret

## 📋 Step 3: Run Database Migration

```bash
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose exec backend alembic upgrade head
```

This will add the Google OAuth fields to your users table.

## 📋 Step 4: Rebuild and Restart

```bash
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose down
docker-compose up --build
```

## 📋 Step 5: Add Frontend Google Sign-In Button

I'll create the frontend component next. The flow will be:

1. User clicks "Sign in with Google"
2. Redirects to Google login
3. User authorizes the app
4. Google redirects back to your app
5. Backend creates/updates user and generates JWT
6. Frontend receives token and logs user in

## 🎨 Frontend Implementation (Next Step)

I'll add:
1. Google Sign-In button on Login page
2. Google Sign-In button on Register page
3. OAuth callback handler page
4. Token storage and auto-login

## 🧪 Testing Google Auth

Once setup is complete:

1. Go to http://localhost:5173
2. Click "Sign in with Google"
3. Select your Google account
4. Authorize the app
5. You'll be redirected back and automatically logged in!

## 🔒 Security Notes

1. **Client Secret**: Keep this secret! Never commit to Git
2. **HTTPS in Production**: Use HTTPS URLs for production
3. **Authorized Domains**: Only add trusted domains
4. **Token Expiry**: JWT tokens expire after 24 hours

## 📊 How It Works

```
User clicks "Sign in with Google"
         ↓
Frontend calls: GET /api/v1/auth/google/login
         ↓
Backend returns Google OAuth URL
         ↓
User redirected to Google login
         ↓
User authorizes app
         ↓
Google redirects to: /api/v1/auth/google/callback?code=xxx
         ↓
Backend exchanges code for access token
         ↓
Backend gets user info from Google
         ↓
Backend creates/updates user in database
         ↓
Backend generates JWT token
         ↓
Backend redirects to: /auth/callback?token=xxx
         ↓
Frontend stores token and logs user in
         ↓
User is authenticated!
```

## 🎯 Benefits

1. **No Password Required**: Users don't need to remember another password
2. **Faster Registration**: One-click sign up
3. **Secure**: Leverages Google's security
4. **Profile Picture**: Automatically gets user's Google profile picture
5. **Email Verified**: Google emails are already verified

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
- Check that redirect URI in Google Console matches exactly:
  `http://localhost:8000/api/v1/auth/google/callback`

### Error: "invalid_client"
- Check that Client ID and Client Secret are correct in `.env`

### Error: "access_denied"
- User cancelled the authorization
- Or app is not approved (add user as test user)

### Error: "Failed to obtain access token"
- Check Client Secret is correct
- Check redirect URI matches

## 📝 Next Steps

1. ✅ Complete Google Cloud Console setup
2. ✅ Add credentials to `.env` file
3. ✅ Run database migration
4. ✅ Rebuild containers
5. ⏳ I'll add the frontend Google Sign-In button
6. ⏳ Test the complete flow

---

**Ready to proceed?** Let me know when you've completed Steps 1-4, and I'll add the frontend Google Sign-In button!
