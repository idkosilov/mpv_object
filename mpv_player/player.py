from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpv import MPV
from renderer import MpvRenderer

QML_IMPORT_NAME = "mpvplayer"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvPlayer(QQuickFramebufferObject):
    do_update = Signal()

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.mpv_instance = MPV(vo='libmpv')
        self._renderer = None
        self.do_update.connect(self.update)

    @Slot(str)
    def play(self, url: str) -> None:
        self.mpv_instance.play(url)

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        self._renderer = MpvRenderer(self)
        return self._renderer

    def __del__(self):
        self.do_update.disconnect(self.update)
        del self._renderer
        del self.mpv_instance
