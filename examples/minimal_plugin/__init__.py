def classFactory(iface):
    """Return the plugin instance used by QGIS."""
    from .plugin import MinimalPlugin
    return MinimalPlugin(iface)
