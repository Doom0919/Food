# 🚀 Quick Deploy Guide - food.careby.app

## Серверт deploy хийх (зөвхөн 3 алхам)

### 1️⃣ Deploy хийх
```bash
chmod +x deploy.sh
./deploy.sh
```

### 2️⃣ SSL сертификат авах
```bash
# Эхлээд имэйл хаягаа оруулах
nano init-letsencrypt.sh
# email="" мөрийг: email="your-email@example.com" болгох

# Дараа нь ажиллуулах
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

### 3️⃣ Шалгах
```bash
# Logs харах
docker-compose logs -f web

# Эсвэл browser дээр:
https://food.careby.app
```

---

## Тусламж команд

```bash
# Container статус
docker-compose ps

# Logs харах
docker-compose logs -f web
docker-compose logs -f nginx

# Дахин эхлүүлэх
docker-compose restart

# Зогсоох
docker-compose down

# Database backup
docker-compose exec db pg_dump -U postgres food_db > backup.sql

# Database restore
cat backup.sql | docker-compose exec -T db psql -U postgres food_db

# Superuser үүсгэх
docker-compose exec web python manage.py createsuperuser
```

---

## Алдаа засах

### SSL сертификат авахад алдаа гарвал:
```bash
# 1. DNS зөв тохируулагдсан эсэхийг шалгах
nslookup food.careby.app

# 2. Nginx зөв ажиллаж байгаа эсэх
docker-compose exec nginx nginx -t

# 3. Certbot logs
docker-compose logs certbot

# 4. Дахин оролдох
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d food.careby.app -d www.food.careby.app \
  --email your-email@example.com \
  --agree-tos --force-renewal
```

### Database холболтын алдаа:
```bash
# Database container ажиллаж байгаа эсэх
docker-compose ps db

# Database logs
docker-compose logs db

# Database руу нэвтрэх
docker-compose exec db psql -U postgres -d food_db
```

### Static файлууд ачаалагдахгүй байвал:
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

---

## Environment Variables

Production дээр environment variables тохируулах:

```bash
# .env файл үүсгэх
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=your-very-secret-key-here-change-this
ALLOWED_HOSTS=food.careby.app,www.food.careby.app
DB_HOST=db
DB_NAME=food_db
DB_USER=postgres
DB_PASSWORD=your-strong-password-here
DB_PORT=5432
EOF

# docker-compose.yml файлд env_file нэмэх
# web service дээр:
#   env_file:
#     - .env
```

---

## Firewall тохиргоо

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

**🎯 Бүх зүйл амжилттай!**
