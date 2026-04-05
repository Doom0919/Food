#!/bin/bash

set -e

echo "======================================"
echo "Food App Deployment Script"
echo "======================================"
echo ""

# 1. Create requirements.txt with correct encoding
echo "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
Django==6.0.3
django-stubs==6.0.2
django-stubs-ext==6.0.2
django-unfold==0.87.0
djangorestframework==3.17.1
djangorestframework-stubs==3.16.9
psycopg2==2.9.11
psycopg2-binary==2.9.11
gunicorn==23.0.0
EOF

# 2. Create nginx folders
echo "Creating nginx and certbot directories..."
mkdir -p nginx/conf.d certbot/conf certbot/www

# 3. Copy nginx configs
echo "Copying nginx configuration files..."
cp nginx_nginx.conf nginx/nginx.conf
cp nginx_food.conf nginx/conf.d/food.conf

# 4. Stop existing containers
echo "Stopping existing containers..."
docker-compose down || true

# 5. Build and start containers
echo "Building Docker images..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up -d

# 6. Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# 7. Run migrations
echo "Running database migrations..."
docker-compose exec -T web python manage.py migrate

# 8. Collect static files
echo "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

# 9. Check status
echo ""
echo "======================================"
echo "Deployment Status"
echo "======================================"
docker-compose ps

echo ""
echo "======================================"
echo "Recent Logs"
echo "======================================"
docker-compose logs --tail=20 web

echo ""
echo "✅ Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Check if containers are running: docker-compose ps"
echo "2. View logs: docker-compose logs -f web"
echo "3. For SSL certificate, run: ./init-letsencrypt.sh"
echo ""
