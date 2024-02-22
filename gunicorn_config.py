import multiprocessing

bind = "0.0.0.0:5004"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60 * 12
capture_output = True
enable_stdio_inheritance = True
loglevel = "debug"

# We trust the environment around the container
# in production: the VM's firewall is not open on port 8000
forwarded_allow_ips = "*"
