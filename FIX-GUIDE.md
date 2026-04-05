# 🐛 Fix: Windows Import Error

## Problem
`core/models.py` файлд Windows-only import байсан:
```python
from asyncio.windows_events import NULL  # ❌ Linux дээр ажиллахгүй
```

## Solution

### Option 1: Quick Fix (нэг мөр)
```bash
chmod +x fix-and-deploy.sh && ./fix-and-deploy.sh
```

### Option 2: Manual Fix

**1. core/models.py засах:**
```bash
nano core/models.py
```

Эхний мөрийг устгах:
```python
from asyncio.windows_events import NULL  # ← Энийг устга
```

Эсвэл sed ашиглаж:
```bash
sed -i '1d' core/models.py
```

**2. Rebuild & restart:**
```bash
docker-compose down
docker-compose up -d --build
docker-compose exec web python manage.py migrate
```

**3. Check logs:**
```bash
docker-compose logs -f web
```

## Expected Result

Одоо ажиллах ёстой:
```
http://your-server-ip:8000
```

Logs ийм харагдана:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Django version 6.0.3, using settings 'food.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

## Why This Happened

Windows дээр хөгжүүлэлт хийхдээ `asyncio.windows_events` import хийсэн байсан. 
NULL утга нь кодонд ашиглагдаагүй байгаа тул устгаад л болно.
