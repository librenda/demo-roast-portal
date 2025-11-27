# Deploying to Vercel

This guide will help you deploy the Akatos Pitch Roast app to Vercel.

## Prerequisites

1. A Vercel account (free tier works fine)
2. Vercel CLI installed: `npm i -g vercel`
3. (Optional but recommended) Vercel KV for persistent storage

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect the configuration
6. Click "Deploy"

### Option 2: Deploy via CLI

```bash
# Install Vercel CLI if you haven't
npm i -g vercel

# Deploy
vercel

# Follow the prompts to link your project
```

## Setting Up Vercel KV (Required)

**Important**: Without Vercel KV, data won't persist between serverless function invocations. You MUST set up KV for the app to work properly.

1. In your Vercel dashboard, go to your project
2. Go to "Storage" → "Create Database"
3. Select "KV" (Key-Value store)
4. Create a new KV database
5. Link it to your project

6. **Environment Variables are Auto-Configured**: 
   - Vercel automatically injects `KV_REST_API_URL` and `KV_REST_API_TOKEN`
   - The API functions already use these (no additional setup needed!)

7. That's it! The functions in `api/storage/` are already configured to use Vercel KV via the REST API.

## Alternative: Using a Database

If you prefer a full database, you can use:
- **Vercel Postgres** (recommended for production)
- **MongoDB Atlas** (free tier available)
- **Supabase** (free tier available)

You'll need to update the API functions to use your chosen database.

## File Structure for Vercel

```
akatos-judge-app/
├── api/
│   ├── storage/
│   │   ├── list.py
│   │   ├── get.py
│   │   ├── set.py
│   │   └── delete.py
│   └── red-x/
│       └── list.py
├── judge-form.html
├── judge-dashboard.html
├── vercel.json
└── requirements-vercel.txt
```

## Testing Locally

You can test the Vercel functions locally:

```bash
# Install Vercel CLI
npm i -g vercel

# Run local dev server
vercel dev
```

This will start a local server that mimics Vercel's environment.

## Environment Variables

If you're using Vercel KV, the following environment variables are automatically set:
- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`
- `KV_REST_API_READ_ONLY_TOKEN`

## Troubleshooting

### Data Not Persisting

- Make sure you've set up Vercel KV
- Check that the `vercel_kv` module is available in your functions
- Verify environment variables are set correctly

### CORS Issues

- The API functions already include CORS headers
- If you still have issues, check your browser console

### Functions Not Working

- Check Vercel function logs in the dashboard
- Make sure your Python functions follow the Vercel serverless function format
- Verify `vercel.json` routing is correct

## Updating the Code

After making changes:

```bash
# Deploy updates
vercel --prod
```

Or push to your connected Git branch and Vercel will auto-deploy.

## Cost

- **Vercel Hobby (Free)**: 
  - Unlimited serverless function invocations
  - 100GB bandwidth
  - Perfect for this app!

- **Vercel KV**: 
  - Free tier: 256MB storage, 30M reads/day, 10M writes/day
  - More than enough for a pitch competition!

## Need Help?

- [Vercel Docs](https://vercel.com/docs)
- [Vercel KV Docs](https://vercel.com/docs/storage/vercel-kv)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)

