echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Waiting for rabbitmq..."

while ! nc -z rabbitmq 5672; do
  sleep 0.1
done

echo "rabbitmq started"

exec "$@"