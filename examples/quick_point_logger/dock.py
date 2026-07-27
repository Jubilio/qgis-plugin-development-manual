from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class QuickPointDock(QDockWidget):
    captureToggled = pyqtSignal(bool)
    undoRequested = pyqtSignal()
    exportRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Quick Point Logger", parent)
        self.setObjectName("QuickPointLoggerDock")

        container = QWidget(self)
        layout = QVBoxLayout(container)

        self.note_edit = QLineEdit()
        self.note_edit.setPlaceholderText("Note for the next point")
        layout.addWidget(self.note_edit)

        self.summary = QLabel("No points captured")
        layout.addWidget(self.summary)

        row = QHBoxLayout()
        self.capture_button = QPushButton("Start capture")
        self.capture_button.setCheckable(True)
        self.capture_button.toggled.connect(self._toggle)
        row.addWidget(self.capture_button)

        undo = QPushButton("Undo last")
        undo.clicked.connect(self.undoRequested.emit)
        row.addWidget(undo)
        layout.addLayout(row)

        export = QPushButton("Export GeoJSON")
        export.clicked.connect(self.exportRequested.emit)
        layout.addWidget(export)

        self.setWidget(container)

    def _toggle(self, enabled):
        self.capture_button.setText("Stop capture" if enabled else "Start capture")
        self.captureToggled.emit(enabled)

    def set_count(self, count):
        self.summary.setText(f"{count} captured point(s)")
