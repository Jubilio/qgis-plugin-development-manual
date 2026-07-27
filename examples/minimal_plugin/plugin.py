from qgis.PyQt.QtWidgets import QAction


class MinimalPlugin:
    MENU = "&Minimal Plugin Example"

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        self.action = QAction("Run minimal plugin", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToVectorMenu(self.MENU, self.action)
        self.iface.addToolBarIcon(self.action)

    def run(self):
        self.iface.messageBar().pushInfo(
            "Minimal Plugin Example",
            "The plugin lifecycle is working.",
        )

    def unload(self):
        if self.action is None:
            return
        self.iface.removePluginVectorMenu(self.MENU, self.action)
        self.iface.removeToolBarIcon(self.action)
        self.action.deleteLater()
        self.action = None
