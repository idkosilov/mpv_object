from PySide6.QtCore import QSize
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQuick import QQuickFramebufferObject
from mpv import MpvGlGetProcAddressFn, MpvRenderContext

from render_context import RenderContext


class MpvRenderer(QQuickFramebufferObject.Renderer):

    def __init__(self, mpv_player: 'MpvPlayer'):
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
