# to tune see http://gunicorn-docs.readthedocs.org/en/latest/settings.html

import multiprocessing, os
from settings import Config

#
# gevent.monkey issue
#
#https://github.com/gevent/gevent/issues/1016
#
# import gevent.monkey
# gevent.monkey.patch_all()

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#


bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')

backlog = 500

# for nginx or other proxy:
# bind = "unix:/deploy/run/gunicorn.sock"

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#       Defaults is 30.  This is how long the master will wait to hear from a worker
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#
# 

# workers = os.getenv('GUNICORN_WORKERS', (multiprocessing.cpu_count()))
workers = os.getenv('GUNICORN_WORKERS', Config.G_WORKERS)

# --max-requests 的適合值可能會根據你的應用程式特性和工作負載有所不同。這個選項的主要目的是防止長期運行的 worker 因為可能的記憶體洩漏而消耗過多的資源。
max_requests =1000 
# --max-requests-jitter 是 Gunicorn 的一個設定選項，用於在 --max-requests 的基礎上添加一些隨機變化。此選項的目的是防止所有 worker 在同一時間重啓。
max_requests_jitter=100

#處理請求的工作線程數，使用指定數量的線程運行每個worker。為正整數，默認為1。
#--threads 参数只会影响到 gthread worker class, 其他的 worker 是不受这个参数影响的
# threads = 1

# 在 Gunicorn 中，preload_app 參數是一個布林值配置選項，
# 用於控制是否在啟動工作進程(worker processes)前預先加載應用程式。
# 開啟此選項 (preload_app=True) 可以提升啟動速度並節省記憶體使用，
# 但也有其限制和潛在問題。以下是 preload_app 的一些關鍵點和用途

# should save some memory:
preload_app = True

# worker_class
#   sync (default)
#   eventlet 
#   gevent (best)
#   tornado
worker_class = 'sync'
# only relevant for async workers:

worker_connections = 500

#接收到restart信号后，worker可以在graceful_timeout时间内，继续处理完当前requests
graceful_timeout = 90

timeout = 90

#
#   spew - Install a trace function that spews every line of Python
#       that is executed when running the server. This is the
#       nuclear option.
#
#       True or False
#
#spew = False

#
# Server mechanics
#
#   daemon - Detach the main Gunicorn process from the controlling
#       terminal with a standard fork/fork sequence.
#
#       True or False
#
#   raw_env - Pass environment variables to the execution environment.
#
#   pidfile - The path to a pid file to write
#
#       A path string or None to not write a pid file.
#
#   user - Switch worker processes to run as this user.
#
#       A valid user id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getpwnam(value) or None
#       to not change the worker process user.
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
#
#   umask - A mask for file permissions written by Gunicorn. Note that
#       this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string
#       compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid
#       for decimal, hex, and octal representations)
#
#   tmp_upload_dir - A directory to store temporary request data when
#       requests are read. This will most likely be disappearing soon.
#
#       A path to a directory where the process owner can write. Or
#       None to signal that Python should choose one on its own.
#

#daemon = False
#raw_env = [
#    'DJANGO_SECRET_KEY=something',
#    'SPAM=eggs',
#]
#umask = 0
#user = None
#group = None
#tmp_upload_dir = None
# where to store the PID file:
pidfile = './log/gunicorn.pid'

# set this if workers appear to leak memory or have some other longer-lived
# problem. Then they'll automatically restart after they've serviced this many
# requests:
# max_requests = 1000


#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

#errorlog = '-'
#loglevel = 'info'
#accesslog = '-'
#access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# accesslog = './log/gunicorn.access.log'
# errorlog = './log/gunicorn.error.log'
# loglevel = 'info'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


#
# Process naming
#
#   proc_name - A base to use with setproctitle to change the way
#       that Gunicorn processes are reported in the system process
#       table. This affects things like 'ps' and 'top'. If you're
#       going to be running more than one instance of Gunicorn you'll
#       probably want to set a name to tell them apart. This requires
#       that you install the setproctitle module.
#
#       A string or None to choose a default of something like 'gunicorn'.
#

proc_name = None

# only use for development:
# reload = True

# for performance:
keepalive = os.getenv('GUNICORN_KEEPALIVE', 3)

#
# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance
#       as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary
#       master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#

def post_fork(server, worker):
    #server.log.info("Worker spawned (pid: %s)", worker.pid)
    pass

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    pass


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")

# lock = multiprocessing.Lock()

# def pre_request(worker, req):
#     req.headers.append(('FLASK_LOCK', lock))
 

