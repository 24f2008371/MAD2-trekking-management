# MAD2-Trekking-Management-Portal
24f2008371 - Ridhi Sehgal - MAD2 project may 2026 - Trekking Management V2

# Terminal 1: Start the worker
celery -A app.celery worker --loglevel=info
# Terminal 2: Start the beat scheduler
celery -A app.celery beat --loglevel=info

cd frontend
npm install 
npm run build
npm run dev

pip install -r backend/requirements.txt
pip freeze > requirements.txt

python3 -m venv env
source env/bin/activate 🔌

~/go/bin/MailHog

sudo service redis-server start 🟢

celery -A app.celery worker --loglevel=info 👷‍♂️

celery -A app.celery beat --loglevel=info ⏰


