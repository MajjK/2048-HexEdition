from PySide2.QtCore import *
import traceback
import sys


class threadSignals(QObject):
    error = Signal(tuple)
    update = Signal(object)
    finish = Signal(object)


class thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = threadSignals(None)
        self.kwargs['update_callback'] = self.signals.update
        self.kwargs['finish_callback'] = self.signals.finish

    @Slot(name="multithreading")
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except traceback as e:
            e.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, e.format_exc()))
