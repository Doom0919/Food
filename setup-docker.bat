@echo off
REM Энэ скрипт нь Docker контейнеруудыг эхлүүлж, Let's Encrypt SSL сертификат авна

echo Creating nginx and certbot directories...
if not exist nginx mkdir nginx
if not exist nginx\conf.d mkdir nginx\conf.d
if not exist certbot mkdir certbot
if not exist certbot\conf mkdir certbot\conf
if not exist certbot\www mkdir certbot\www

echo Copying nginx configuration files...
copy /Y nginx_nginx.conf nginx\nginx.conf
copy /Y nginx_food.conf nginx\conf.d\food.conf
copy /Y requirements_new.txt requirements.txt

echo.
echo ========================================
echo SETUP INSTRUCTIONS
echo ========================================
echo.
echo 1. Серверийн DNS тохиргоонд food.careby.app болон www.food.careby.app домайнуудыг серверийн IP хаяг руу зааж өгнө үү
echo.
echo 2. Docker containers эхлүүлэх:
echo    docker-compose up -d
echo.
echo 3. Өгөгдлийн сангийн migration хийх:
echo    docker-compose exec web python manage.py migrate
echo    docker-compose exec web python manage.py collectstatic --noinput
echo.
echo 4. Linux серверт SSL сертификат авахын тулд init-letsencrypt.sh скрипт ашиглана:
echo    - Скриптэд өөрийн имэйл хаягаа оруулна уу
echo    - chmod +x init-letsencrypt.sh
echo    - ./init-letsencrypt.sh
echo.
echo 5. Windows дээр бол Docker Desktop ашиглаж байгаа тул локал тестэд өөр сертификат шаардлагатай
echo.
pause
