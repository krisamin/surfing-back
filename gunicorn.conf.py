# surfing-back/gunicorn.conf.py

import multiprocessing

workers = 4
bind = '0.0.0.0:8000'
errorlog = '/log/error.log'
worker_class = 'uvicorn.workers.UvicornWorker'
capture_output = True
loglevel = 'debug'
disable_redirect_access_to_syslog=True