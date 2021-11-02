# web: uvicorn heroku.main:app --host 0.0.0.0 --port $PORT
web: gunicorn heroku.main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT