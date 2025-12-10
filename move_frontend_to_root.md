# Alternative: Move Frontend to Root

Jika vercel.json tidak berhasil, jalankan commands ini:

```bash
# Backup current structure
cp -r frontend frontend_backup

# Move frontend files to root
mv frontend/* .
mv frontend/.* . 2>/dev/null || true

# Remove empty frontend folder
rmdir frontend

# Update package.json scripts if needed
# Update any relative paths in code
```

**Files yang perlu dipindah:**
- package.json
- next.config.js
- tailwind.config.js
- postcss.config.js
- pages/
- components/
- styles/

**Update paths in:**
- Any import statements
- Configuration files
- API calls to backend