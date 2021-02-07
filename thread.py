from PySide2.QtCore import *
import traceback
import sys


class threadSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    game = Signal(object)


class thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = threadSignals()
        self.kwargs['game_callback'] = self.signals.game

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()