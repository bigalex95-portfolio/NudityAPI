# web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
web: gunicorn app.main:APP -w 3 -k uvicorn.workers.UvicornWorker