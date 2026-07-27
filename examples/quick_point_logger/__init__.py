def classFactory(iface):
    from .plugin import QuickPointLoggerPlugin
    return QuickPointLoggerPlugin(iface)
