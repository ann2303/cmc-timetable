docker compose up -d
until curl --output /dev/null --silent --fail http://localhost:8000/health; do
    printf '.'
    sleep 5
done
pytest .
docker compose down
