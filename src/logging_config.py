import os
import logging
from datetime import datetime

logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# Lazy initialization for the log file
log_file = None
file_handler = None

# Temporary storage for logs before a file is created
buffered_logs = []

# Configuration for environments
ENABLE_FILE_LOGGING = True  # Enable file logging in both environments


def setup_logging(env="PROD"):
    """
    Set up the logging configuration based on the environment.
    """
    global logs_dir

    if env == "DEV":
        logs_dir = None  # No logs directory in DEV
    else:
        # Logs directory path set for PROD
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")

    # Configure logging
    handlers = [logging.StreamHandler()]  # Always output logs to the console
    if env == "PROD":
        handlers.append(BufferedHandler())  # Buffer logs for file creation in PROD

    logging.basicConfig(
        level=logging.DEBUG if env == "DEV" else logging.INFO,
        format="%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        handlers=handlers,
    )

    # Add a filter to dynamically trigger log file creation for errors in PROD
    if env == "PROD":
        logging.getLogger().addFilter(FileCreationFilter())


def create_log_file():
    """
    Creates the log file and flushes buffered logs into it.
    """
    global log_file, file_handler

    if not ENABLE_FILE_LOGGING or log_file is not None:
        return  # Skip if file logging is disabled or already initialized

    # Generate a log file name with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(logs_dir, f"budget_tracker_{timestamp}.log")

    # Create and configure the file handler
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Log all levels to the file
    file_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    # Write buffered logs to the file
    for record in buffered_logs:
        file_handler.emit(record)

    # Clear the buffered handler to prevent infinite replay
    root_logger.removeHandler(BufferedHandler())


class BufferedHandler(logging.Handler):
    """
    Custom logging handler to buffer logs until a file is created.
    """

    def emit(self, record):
        buffered_logs.append(record)


class FileCreationFilter(logging.Filter):
    """
    Logging filter to trigger log file creation on error-level logs.
    """

    def filter(self, record):
        if record.levelno >= logging.ERROR:
            create_log_file()
        return True
