from OCC.Display import OCCViewer
from OCC.Display.backend import get_qt_modules, load_backend

backend_str = "qt-pyqt5"
used_backend = load_backend(backend_str)

if 'qt' in used_backend:
    from OCC.Display.qtDisplay import qtViewer3d

    QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()


    class _viewer_(qtViewer3d):

        def __init__(self):
            qtViewer3d.__init__(self)

        def init2(self):
            self._display = CustomOCCViewer3d(self.GetHandle())
            self._display.Create()
            self._display.display_trihedron()
            self._display.SetModeShaded()
            self._SetupKeyMap()

        def top_view(self):
            self._display.View.SetProj(0, 0, 1)

        def side_view(self):
            self._display.View.SetProj(0,1, 0)

        def end_view(self):
            self._display.View.SetProj(1,0, 0)

        def localize_camera(self):
            self._display.View.SetProj(-1, -1, 1)
            self._display.View.SetAt(0, 0, 0)
            self._display.View.SetScale(100)

        def add(self, shape, color=None, transparency=None):
            if shape:
                if color is None and transparency is None:
                    self._display.DisplayShape(shape)
                elif color is None and transparency is not None:
                    self._display.DisplayShape(shape, transparency=transparency)
                elif color is not None and transparency is None:
                    self._display.DisplayShape(shape, color=color)
                else:
                    self._display.DisplayShape(shape, color=color, transparency=transparency)

        def eraseAll(self):
            self._display.EraseAll()

        def remove(self, shape):
            if shape:
                self._display.EraseShape(shape)
                self._display.Repaint()


    class CustomOCCViewer3d(OCCViewer.Viewer3d):

        def __init__(self, *args, **kwargs):
            OCCViewer.Viewer3d.__init__(self, *args, **kwargs)
            self.ShapeMap = {}

        def DisplayShape(self, shapes, **kwargs):

            if isinstance(shapes, (list, tuple)):
                ais_shapes = OCCViewer.Viewer3d.DisplayShape(self, shapes, **kwargs)
                for s, ais in zip(shapes, ais_shapes):
                    self.ShapeMap[s] = ais
            else:
                ais = OCCViewer.Viewer3d.DisplayShape(self, shapes, **kwargs)
                self.ShapeMap[shapes] = ais

        def EraseShape(self, shape):
            if shape not in self.ShapeMap:
                pass
            else:
                self.Context.Erase(self.ShapeMap[shape].GetHandle())

                del self.ShapeMap[shape]
