from PySide6.QtCore import QObject, Slot, QSize
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpv import MPV, MpvRenderContext, MpvGlGetProcAddressFn
from render_context import RenderContext

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

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        self._renderer = MpvRenderer(self)
        return self._renderer


class MpvRenderer(QQuickFramebufferObject.Renderer):

    def __init__(self, mpv_player: MpvPlayer):
        super().__init__()
        self._mpv_player = mpv_player
        self._get_proc_address_function = MpvGlGetProcAddressFn(RenderContext().get_proc_address)
        self.render_context = None

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self.render_context is None:
            self.render_context = MpvRenderContext(
                self._mpv_player.mpv_instance,
                api_type='opengl',
                opengl_init_params={'get_proc_address': self._get_proc_address_function}
            )

            self.render_context.update_cb = self._mpv_player.update

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def render(self) -> None:
        if self.render_context is not None:
            rectangle = self._mpv_player.size()
            width = int(rectangle.width())
            height = int(rectangle.height())
            fbo = int(self.framebufferObject().handle())
            self.render_context.render(flip_y=False, opengl_fbo={"w": width, "h": height, "fbo": fbo})