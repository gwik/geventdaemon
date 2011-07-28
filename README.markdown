**geventdaemon** is a wrapper around python-daemon to help daemonizing gevent based processes.

It delegates the signal handling to gevent instead of using python's
and reinit the event loop after forks.

Specific options :

`monkey`, None by default, it can be a dict or
something that evaluate to True.
If it is True, it patches all. (gevent.monkey.patch_all()).
If it is a dict, it pass the dict as keywords arguments to patch_all().

`signal_map` receives a dict of signals, but handler is either a
callable, a list of arguments [callable, arg1, arg2] or
a string.
callable without arguments will receive (signal, None) as arguments,
meaning the `frame` parameter is always None.

usage:

    from geventdaemon import GeventDaemonContext
    def work()
        gevent.sleep(500)

    def stop(signal, frame):
        # frame is always None, it is there for compatibility with python-daemon
        raise SystemExit('terminated by signal %d' % int(signal))

    context = GeventDaemonContext(monkey={'httplib': True},
        signal_map={signal.SIGTERM: stop,
                    signal.SIGINT: stop})

    with context:
        # do some gevent work after fork.
        work()

