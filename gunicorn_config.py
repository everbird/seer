#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep
import sys
import os
from os.path import join, dirname, abspath
import signal
import threading

from config.config import setup_logs, SITE_PORT

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "0.0.0.0:%s" % SITE_PORT
workers = 2 #numCPUs() * 2 + 1
keepalive = 4
loglevel = 'info'
backlog = 2048
# for production
#worker_class = "gevent"
#debug = False
# for dev
worker_class = "sync"
debug = True
daemon = False # MUST be False when use gunicorn with supervisord
pidfile = os.path.expanduser('~/var/%s/run/gunicorn-%s.pid' % (SITE_PORT, SITE_PORT))
errorlog = os.path.expanduser('~/var/%s/log/gunicorn-error-%s.log' % (SITE_PORT, SITE_PORT))
accesslog = os.path.expanduser('~/var/%s/log/gunicorn-access-%s.log' % (SITE_PORT, SITE_PORT))
logfile = os.path.expanduser('~/var/%s/log/gunicorn-output-%s.log' % (SITE_PORT, SITE_PORT))

current_dir = os.getcwd()

start_time = time()

def when_ready(server):
    """Gunicorn server ready hook
    """

    Reloader(server).start()
    setup_logs()

class WalkReloader(threading.Thread):
    """Auto reloader for auto-reloading gunicorn workers when .py file modified
    """

    def __init__(self, server):
        self.server = server
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        modify_times = {}
        current_dir = dirname(abspath(__file__))

        for root, dirs, files in os.walk(current_dir):
            for _file in (join(root, name) for name in files):
                if _file.endswith('.py'):
                    modify_times[_file] = os.stat(_file).st_mtime

        while True:
            for _file, mtime in modify_times.iteritems():
                try:
                    if mtime != os.stat(_file).st_mtime:
                        print '%s modified, reload workers...' % _file
                        os.kill(self.server.pid, signal.SIGHUP)
                        modify_times[_file] = os.stat(_file).st_mtime
                except (OSError):
                    del(modify_times[_file])
                    break
            sleep(2)

try:
    import pyinotify

    RELOAD_THRESHOLD = 0.2

    def my_filter(p):
        return '.svn' in p

    class MyEventHandler(pyinotify.ProcessEvent):
        def my_init(self, pid):
            self._pid = pid
            self._timer = None

        def process_default(self, event):
            f = event.pathname
            if f.endswith('.py'):
                print '%s modifed' % f

                if self._timer and self._timer.is_alive():
                    self._timer.cancel()

                self._timer = threading.Timer(RELOAD_THRESHOLD, self._do_rst)
                self._timer.start()

        def _do_rst(self):
            print 'reload workers'
            os.kill(self._pid, signal.SIGHUP)

    class INotifyReloader(object):
        """Auto reloader employ inotify(7)
        """

        def __init__(self, server):
            self.server = server

        def start(self):
            wm = pyinotify.WatchManager()
            eh = MyEventHandler(pid=self.server.pid)

            notifier = pyinotify.ThreadedNotifier(wm, eh)
            notifier.daemon = True
            notifier.start()

            mask = pyinotify.IN_MODIFY | pyinotify.IN_CREATE | pyinotify.IN_DELETE \
                    | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM

            def _add(path, rec=False):
                wm.add_watch(path, mask, rec=rec,
                        auto_add=True, exclude_filter=my_filter)

            _add(current_dir, rec=True)

            cost = time() - start_time
            print >> sys.stderr, 'reloader ready, cost: %.3fs' % cost

    Reloader = INotifyReloader

except ImportError:
    Reloader = WalkReloader
