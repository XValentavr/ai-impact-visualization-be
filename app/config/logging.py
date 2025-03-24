import logging

from loguru import logger

from app.config.settings import settings

LOGGERS = (
    "uvicorn",
    "uvicorn.access",
    "uvicorn.error",
    "fastapi",
    "asyncio",
    "starlette",
)

# Remove every handler associated with the root logger object
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller to get correct stack depth
        frame, depth = logging.currentframe(), 2
        while frame.f_back and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# Replace handlers of all loggers
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

# Add sinks
logger.add(
    settings.server.LOG_FILE_PATH,
    rotation="500 MB",
    compression="zip",
    level="INFO",
    backtrace=True,
    diagnose=True,
)

for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = []
    logging_logger.propagate = True
