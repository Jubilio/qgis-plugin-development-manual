from qgis.core import QgsApplication, QgsTask


class BatchTask(QgsTask):
    def __init__(self, items, callback):
        flags = getattr(QgsTask, "Flag", None)
        can_cancel = flags.CanCancel if flags else QgsTask.CanCancel
        super().__init__("Batch task", can_cancel)
        self.items = list(items)
        self.callback = callback
        self.results = []
        self.error = None

    def run(self):
        try:
            total = max(1, len(self.items))
            for index, item in enumerate(self.items, 1):
                if self.isCanceled():
                    return False
                self.results.append(self.process(item))
                self.setProgress(index / total * 100)
            return True
        except Exception as exc:
            self.error = exc
            return False

    def process(self, item):
        return item

    def finished(self, success):
        self.callback(self, success)


def start(items, callback):
    task = BatchTask(items, callback)
    QgsApplication.taskManager().addTask(task)
    return task
