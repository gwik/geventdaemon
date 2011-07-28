*geventdaemon* is a wrapper around python-daemon to help daemonizing gevent based processes.

It delegates the signal handling to gevent instead of using python's.
It reinit the event loop after forks.

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

