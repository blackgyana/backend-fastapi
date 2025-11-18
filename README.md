docker network create booking-network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=booking-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking-network \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=booking-network \
    booking_image


docker run --name booking_celery_worker \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .


docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=booking-network \
    --rm -p 80:80 nginx
    --rm -p 80:80 -p 443:443 nginx