# 🚀 BeatLens Deployment Guide

## 📋 Prerequisites

- GitHub account
- Vercel account (for frontend)
- Railway account (for backend)

## 🎯 Step-by-Step Deployment

### 1️⃣ Deploy Backend to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Connect GitHub** and select `BeatLens` repository
3. **Configure deployment:**
   - Root Directory: `backend`
   - Start Command: `python db/init_db.py && uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: (none required for basic setup)

4. **Deploy and get URL** (e.g., `https://beatlens-backend-production.up.railway.app`)

### 2️⃣ Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)**
2. **Import from GitHub** - select `BeatLens` repository
3. **Configure project:**
   - Framework Preset: `Next.js`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Add Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
   NEXT_PUBLIC_APP_ENV=production
   ```

5. **Deploy**

### 3️⃣ Update CORS (if needed)

If you get CORS errors, update `backend/app.py`:

```python
allow_origins=[
    "https://your-vercel-app.vercel.app",  # Your actual Vercel URL
    "https://beatlens.vercel.app",         # Custom domain
]
```

## 🔧 Alternative: Manual Deployment

### Option A: Deploy Frontend Only (Static)

```bash
# Build static version
cd frontend
npm run build
npm run export

# Deploy to Netlify/Vercel/GitHub Pages
# Upload 'out' folder
```

### Option B: Monorepo with Vercel

1. **Use the `vercel.json` we created:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "frontend/package.json",
         "use": "@vercel/next"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "frontend/$1"
       }
     ]
   }
   ```

2. **Deploy entire repository to Vercel**

## 🌐 Custom Domain (Optional)

### For Vercel:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### For Railway:
1. Go to Project Settings → Networking
2. Add custom domain
3. Update DNS records

## 🔍 Troubleshooting

### Common Issues:

1. **404 Error on Vercel:**
   - Check Root Directory is set to `frontend`
   - Verify `vercel.json` configuration
   - Check build logs for errors

2. **CORS Error:**
   - Update `allow_origins` in backend
   - Redeploy backend after changes

3. **API Connection Failed:**
   - Verify `NEXT_PUBLIC_API_URL` environment variable
   - Check backend is deployed and accessible
   - Test backend health endpoint: `/health`

4. **Build Failed:**
   - Check Node.js version compatibility
   - Verify all dependencies in `package.json`
   - Check build logs for specific errors

## 📊 Monitoring

### Health Check Endpoints:
- **Backend**: `https://your-backend-url/health`
- **Frontend**: `https://your-frontend-url` (should load homepage)

### Performance:
- **Backend Response Time**: Should be < 100ms
- **Frontend Load Time**: Should be < 3s
- **API Calls**: Monitor in browser DevTools

## 🎉 Success Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and loading
- [ ] API calls working (test mood selection)
- [ ] Recommendations generating properly
- [ ] No CORS errors in browser console
- [ ] Custom domain configured (if applicable)

## 🆘 Need Help?

1. Check deployment logs in Vercel/Railway dashboard
2. Test API endpoints manually with curl/Postman
3. Verify environment variables are set correctly
4. Check this guide for common solutions

---

**🎵 Once deployed, your BeatLens app will be live and accessible worldwide!**