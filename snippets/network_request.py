from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsNetworkAccessManager


def get_json(url, finished_callback):
    request = QNetworkRequest(QUrl(url))
    request.setRawHeader(b"User-Agent", b"Example-QGIS-Plugin/0.1")
    reply = QgsNetworkAccessManager.instance().get(request)
    reply.finished.connect(lambda: finished_callback(reply))
    return reply
