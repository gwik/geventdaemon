import gevent
import daemon
import os
import signal


class GeventDaemonContext(daemon.DaemonContext):
    """ DaemonContext for gevent.

    Receive same options as a DaemonContext (python-daemon), Except:

    `monkey`: None by default, does nothing. Else it can be a dict or
    something that evaluate to True.
    If it is True, it patches all. (gevent.monkey.patch_all()).
    If it is a dict, it pass the dict as keywords arguments to patch_all().

    `signal_map`: receives a dict of signals, but handler is either a
    callable, a list of arguments [callable, arg1, arg2] or
    a string.
    callable without arguments will receive (signal, None) as arguments,
    meaning the `frame` parameter is always None.

    If the daemon context forks. It calls gevent.reinit().
    """

    def __init__(self, monkey=None, signal_map=None, **daemon_options):
        self.gevent_signal_map = signal_map
        self.monkey = None
        super(GeventDaemonContext, self).__init__(
                signal_map={}, **daemon_options)

    def open(self):
        pid = os.getpid()
        super(GeventDaemonContext, self).open()
        if pid != os.getpid():
            gevent.reinit()
        self._setup_gevent_signals()
        self._apply_monkey_patch()

    def _apply_monkey_patch(self):
        if isinstance(self.monkey, dict):
            gevent.monkey.patch_all(**self.monkey)
        elif self.monkey:
            gevent.monkey.patch_all()

    def _setup_gevent_signals(self):
        if self.gevent_signal_map is None:
            gevent.signal(signal.SIGTERM, self.terminate, signal.SIGTERM, None)
            return

        for sig, target in self.gevent_signal_map.items():
            if target is None:
                raise ValueError(
                        'invalid handler argument for signal %s', str(sig))
            tocall = target
            args = [sig, None]
            if isinstance(target, list):
                if not target:
                    raise ValueError(
                            'handler list is empty for signal %s', str(sig))
                tocall = target[0]
                args = target[1:]
            elif isinstance(target, basestring):
                assert not target.startswith('_')
                tocall = getattr(self, target)

            gevent.signal(sig, tocall, *args)


