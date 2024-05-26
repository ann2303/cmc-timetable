docker compose up -d
pip install -r requirements.txt
until curl --output /dev/null --silent --fail http://localhost:8000/health; do
    printf '.'
    sleep 5
done
pytest .
docker compose down
