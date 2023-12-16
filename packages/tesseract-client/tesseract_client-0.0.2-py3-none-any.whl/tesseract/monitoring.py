from watchdog.events import FileSystemEventHandler
from loguru import logger

from tesseract.services import Services


class FileChangeHandler(FileSystemEventHandler):
    """Handles changes in the monitored folder."""
    def __init__(self, services: Services):
        super().__init__()
        self.services = services
        logger.info("FileChangeHandler initialized")

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"File created: {event.src_path}")
            self.services.create_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"File deleted: {event.src_path}")
            self.services.delete_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified':
            logger.info(f"File modified: {event.src_path}")
            self.services.update_file(event.src_path)
