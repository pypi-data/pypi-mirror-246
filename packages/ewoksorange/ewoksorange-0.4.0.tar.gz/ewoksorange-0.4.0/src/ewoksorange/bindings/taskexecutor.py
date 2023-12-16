import logging
from typing import Optional
from AnyQt.QtCore import QThread
from ewokscore.task import TaskInputError
from ewokscore import TaskWithProgress


_logger = logging.getLogger(__name__)


class TaskExecutor:
    """Create and execute an Ewoks task"""

    def __init__(self, ewokstaskclass):
        self.__ewokstaskclass = ewokstaskclass
        self.__task = None

    def create_task(self, **kwargs):
        if not issubclass(self.__ewokstaskclass, TaskWithProgress):
            kwargs.pop("progress", None)
        self.__task = None
        try:
            self.__task = self.__ewokstaskclass(**kwargs)
        except TaskInputError as e:
            _logger.info(f"task initialization failed: {e}")

    def execute_task(self):
        if not self.has_task:
            return
        try:
            self.__task.execute()
        except Exception as e:
            _logger.error(f"task failed: {e}", exc_info=True)

    @property
    def has_task(self) -> bool:
        return self.__task is not None

    @property
    def succeeded(self) -> Optional[bool]:
        if self.__task is None:
            return None
        return self.__task.succeeded

    @property
    def done(self) -> Optional[bool]:
        if self.__task is None:
            return None
        return self.__task.done

    @property
    def output_variables(self):
        if self.__task is None:
            return dict()
        return self.__task.output_variables

    @property
    def current_task(self):
        return self.__task


class ThreadedTaskExecutor(QThread, TaskExecutor):
    """Create and execute an Ewoks task in a dedicated thread."""

    def run(self):
        self.execute_task()

    def stop(self, timeout=None, wait=False):
        self.blockSignals(True)
        if wait:
            if timeout:
                self.wait(timeout * 1000)
            else:
                self.wait()
        if self.isRunning():
            self.quit()
