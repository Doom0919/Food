# Docker HTTPS Тохиргоо - food.careby.app

## Бэлтгэсэн зүйлс

✅ **Docker-compose конфигурац**
- Nginx reverse proxy нэмсэн (port 80, 443)
- Certbot автомат SSL сертификат сунгалт
- Gunicorn WSGI сервер
- Static файлууд volume

✅ **Django Settings**
- HTTPS тохиргоо нэмсэн
- `food.careby.app` CSRF_TRUSTED_ORIGINS-д нэмсэн
- Security headers (HSTS, SSL redirect)

✅ **Nginx Конфигурац**
- HTTP -> HTTPS redirect
- SSL/TLS тохиргоо
- Static болон media файлууд serve хийх
- Proxy headers Django-руу

## Хэрэглэх заавар

### 1. Nginx конфигурац файлууд хуулах

Windows дээр байгаа тул эхлээд folderууд үүсгээд файлуудыг хуулна уу:

```cmd
setup-docker.bat
```

Эсвэл гараар:

```cmd
mkdir nginx
mkdir nginx\conf.d
mkdir certbot
mkdir certbot\conf
mkdir certbot\www

copy nginx_nginx.conf nginx\nginx.conf
copy nginx_food.conf nginx\conf.d\food.conf
copy requirements_new.txt requirements.txt
```

### 2. DNS тохиргоо

Домайны DNS тохиргоонд дараах recordууд нэмнэ:

```
A Record: food.careby.app -> Таны серверийн IP хаяг
A Record: www.food.careby.app -> Таны серверийн IP хаяг
```

### 3. Docker эхлүүлэх

```bash
# Build and start
docker-compose up -d --build

# Database migration
docker-compose exec web python manage.py migrate

# Collect static files  
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### 4. SSL Сертификат авах (Linux серверт)

Linux сервер дээр бол `init-letsencrypt.sh` скриптийг ашиглана:

1. Скриптэд өөрийн имэйл оруулах:
```bash
nano init-letsencrypt.sh
# email="your-email@example.com" мөрийг засах
```

2. Скрипт ажиллуулах:
```bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

### 5. Шалгах

```bash
# Logs шалгах
docker-compose logs -f web
docker-compose logs -f nginx

# Container статус
docker-compose ps

# Эсвэл browser дээр:
https://food.careby.app
```

## Тэмдэглэл

- Production-д `DEBUG=False` байх ёстой
- SECRET_KEY secure утга ашиглах
- Өгөгдлийн сангийн нууц үгийг солих
- Firewall дээр 80, 443 портуудыг нээх

## Алдаа засах

Хэрэв SSL сертификат алдаа гарвал:

```bash
# Nginx шалгах
docker-compose exec nginx nginx -t

# SSL сертификат байгаа эсэх
docker-compose exec nginx ls -la /etc/letsencrypt/live/food.careby.app/

# Certbot дахин ажиллуулах
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d food.careby.app -d www.food.careby.app \
  --email your-email@example.com \
  --agree-tos --force-renewal
```
