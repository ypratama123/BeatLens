# 🔧 Deployment Troubleshooting Guide

## 🚂 Railway Backend Issues

### ❌ Build Failed
**Symptoms**: Deployment fails during build
**Solutions**:
1. Check `requirements.txt` exists in `/backend`
2. Verify Python version compatibility
3. Check Railway logs: Settings → Deployments → View Logs

### ❌ Database Error
**Symptoms**: "Database not found" or SQLite errors
**Solutions**:
1. Ensure `db/init_db.py` runs in start command
2. Check file permissions
3. Verify `seed_data.json` exists

### ❌ Port Error
**Symptoms**: "Port already in use" or connection refused
**Solutions**:
1. Ensure start command uses `--port $PORT`
2. Check Railway auto-assigns PORT variable
3. Verify CORS settings allow Vercel domain

## ⚡ Vercel Frontend Issues

### ❌ Build Failed
**Symptoms**: Next.js build fails
**Solutions**:
1. Check `package.json` exists in `/frontend`
2. Verify Node.js version compatibility
3. Check build logs in Vercel dashboard

### ❌ API Connection Failed
**Symptoms**: "Failed to fetch" or CORS errors
**Solutions**:
1. Verify `NEXT_PUBLIC_API_URL` environment variable
2. Check Railway backend is running
3. Test backend URL directly: `/health` endpoint

### ❌ 404 Not Found
**Symptoms**: Vercel shows 404 for all routes
**Solutions**:
1. Ensure Root Directory is set to `frontend`
2. Check `pages/` folder structure
3. Verify `next.config.js` configuration

## 🔗 Integration Issues

### ❌ CORS Error
**Symptoms**: "Access blocked by CORS policy"
**Solutions**:
1. Update backend CORS settings:
```python
allow_origins=[
    "https://your-vercel-app.vercel.app",
    "https://beatlens.vercel.app"
]
```
2. Redeploy backend after CORS changes

### ❌ Environment Variables
**Symptoms**: API calls go to localhost
**Solutions**:
1. Check Vercel environment variables
2. Ensure variable name: `NEXT_PUBLIC_API_URL`
3. Redeploy frontend after adding variables

## 🆘 Quick Fixes

### Railway Backend Not Starting:
```bash
# Check start command in Railway settings:
python db/init_db.py && uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Vercel Frontend Not Loading:
```bash
# Check these settings:
Framework: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
```

### API Connection Issues:
1. Test backend: `https://your-railway-url/health`
2. Check frontend env: `NEXT_PUBLIC_API_URL`
3. Verify CORS in backend `app.py`

## 📞 Getting Help

1. **Railway Logs**: Settings → Deployments → View Logs
2. **Vercel Logs**: Project → Functions → View Function Logs
3. **Browser Console**: F12 → Console (for frontend errors)
4. **Network Tab**: F12 → Network (for API call issues)

## ✅ Success Checklist

- [ ] Railway backend deployed and accessible
- [ ] Vercel frontend deployed and loading
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] API calls working (test with mood selection)
- [ ] Recommendations generating properly
- [ ] No console errors in browser