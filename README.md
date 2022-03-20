# stream-url

Stream and proxy links 

pip install aiohttp gunicorn
python main.py
or 
gunicorn main:main --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker
