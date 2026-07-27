from pathlib import Path

from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsSettings,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.gui import QgsMapToolEmitPoint

from .dock import QuickPointDock
from .utils import utc_timestamp


def right_dock_area():
    scoped = getattr(Qt, "DockWidgetArea", None)
    return scoped.RightDockWidgetArea if scoped else Qt.RightDockWidgetArea


class QuickPointLoggerPlugin:
    MENU = "&Quick Point Logger Example"
    SETTINGS = "quick_point_logger"

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.action = None
        self.dock = None
        self.tool = None
        self.layer = None
        self.last_feature_id = None
        self.settings = QgsSettings()

    def initGui(self):
        icon = QIcon(str(Path(__file__).parent / "icons" / "capture.svg"))
        self.action = QAction(icon, "Quick Point Logger", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.toggled.connect(self.activate)
        self.iface.addPluginToVectorMenu(self.MENU, self.action)
        self.iface.addToolBarIcon(self.action)

        self.dock = QuickPointDock(self.iface.mainWindow())
        self.iface.addDockWidget(right_dock_area(), self.dock)
        self.dock.captureToggled.connect(self.activate)
        self.dock.undoRequested.connect(self.undo_last)
        self.dock.exportRequested.connect(self.export_geojson)
        self.dock.note_edit.setText(
            self.settings.value(f"{self.SETTINGS}/note", "", type=str)
        )
        self.dock.hide()

    def activate(self, enabled=True):
        if self.action.isChecked() != enabled:
            self.action.blockSignals(True)
            self.action.setChecked(enabled)
            self.action.blockSignals(False)

        if not enabled:
            if self.tool and self.canvas.mapTool() is self.tool:
                self.canvas.unsetMapTool(self.tool)
            return

        if self.tool is None:
            self.tool = QgsMapToolEmitPoint(self.canvas)
            self.tool.canvasClicked.connect(self.capture_point)
            self.tool.setAction(self.action)

        self.canvas.setMapTool(self.tool)
        self.dock.show()
        self.dock.raise_()

    def ensure_layer(self):
        if self.layer and self.layer.isValid():
            return True
        self.layer = QgsVectorLayer("Point?crs=EPSG:4326", "Quick Point Log", "memory")
        self.layer.dataProvider().addAttributes([
            QgsField("captured_at", QVariant.String),
            QgsField("latitude", QVariant.Double),
            QgsField("longitude", QVariant.Double),
            QgsField("note", QVariant.String),
        ])
        self.layer.updateFields()
        QgsProject.instance().addMapLayer(self.layer)
        return self.layer.isValid()

    def capture_point(self, map_point, _button):
        if not self.ensure_layer():
            return

        project_crs = self.canvas.mapSettings().destinationCrs()
        wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        point = QgsCoordinateTransform(
            project_crs,
            wgs84,
            QgsProject.instance(),
        ).transform(map_point)

        feature = QgsFeature(self.layer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point)))
        feature["captured_at"] = utc_timestamp()
        feature["latitude"] = float(point.y())
        feature["longitude"] = float(point.x())
        feature["note"] = self.dock.note_edit.text().strip()

        ok, created = self.layer.dataProvider().addFeatures([feature])
        if ok and created:
            self.last_feature_id = created[0].id()
            self.layer.updateExtents()
            self.layer.triggerRepaint()
            self.dock.set_count(self.layer.featureCount())
            self.settings.setValue(
                f"{self.SETTINGS}/note",
                self.dock.note_edit.text(),
            )

    def undo_last(self):
        if self.layer is None or self.last_feature_id is None:
            return
        self.layer.dataProvider().deleteFeatures([self.last_feature_id])
        self.last_feature_id = None
        self.layer.triggerRepaint()
        self.dock.set_count(self.layer.featureCount())

    def export_geojson(self):
        if self.layer is None or self.layer.featureCount() == 0:
            return
        path, _ = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            "Export captured points",
            "captured_points.geojson",
            "GeoJSON (*.geojson)",
        )
        if not path:
            return
        if not path.lower().endswith(".geojson"):
            path += ".geojson"

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GeoJSON"
        options.fileEncoding = "UTF-8"
        QgsVectorFileWriter.writeAsVectorFormatV3(
            self.layer,
            path,
            QgsProject.instance().transformContext(),
            options,
        )

    def unload(self):
        if self.tool and self.canvas.mapTool() is self.tool:
            self.canvas.unsetMapTool(self.tool)
        if self.action:
            self.iface.removePluginVectorMenu(self.MENU, self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action.deleteLater()
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock.deleteLater()
