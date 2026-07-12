# MAD2-Trekking-Management-Portal
24f2008371 - Ridhi Sehgal - MAD2 project may 2026 - Trekking Management V2

# Terminal 1: Start the worker
celery -A app.celery worker --loglevel=info
# Terminal 2: Start the beat scheduler
celery -A app.celery beat --loglevel=info