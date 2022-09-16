from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpv import MPV
from mpv_renderer import MpvRenderer


QML_IMPORT_NAME = "mpvplayer"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvPlayer(QQuickFramebufferObject):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.mpv_instance = MPV(vo='libmpv', hwdec='videotoolbox')
        self._renderer = None

    @Slot(str)
    def play(self, url: str) -> None:
        self.mpv_instance.play(url)

    def createRenderer(self) -> 'QQuickFramebufferObject.Renderer':
        self._renderer = MpvRenderer(self)
        return self._renderer
