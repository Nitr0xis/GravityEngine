"""
Logging system for GravityEngine.
====================================

Writes events and errors in user_data/logs/. Designed to diagnose
crashes on .exe builds where the user has no console.

Usage:
    from logger import Logger

    Logger.setup(engine.logs_folder_path)
    Logger.info("Engine initialized")
    Logger.error("Failed to load asset")
    Logger.exception("Unhandled crash")  # to call in an except block, captures the traceback
"""

import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """
    Static wrapper around logging.Logger.

    All methods are static: only one global logger for the whole
    project, initialized once via setup().
    """

    _logger: Optional[logging.Logger] = None
    _log_dir: Optional[str] = None

    @staticmethod
    def setup(log_dir: str, level: int = logging.INFO, max_bytes: int = 1_000_000, backup_count: int = 3) -> None:
        """
        Initializes the logger. Should be called only once, early in Engine.__init__,
        just after the creation of the 'logs' folder by the FileManager.

        Args:
            log_dir: path to the logs folder (engine.logs_folder_path)
            level: minimum logging level (default: logging.INFO)
            max_bytes: max size of a log file before rotation
            backup_count: number of rotated log files to keep
        """
        if Logger._logger is not None:
            # Already initialized, don't do anything (prevents duplicate handlers)
            return

        Logger._log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, "gravityengine.log")

        logger = logging.getLogger("GravityEngine")
        logger.setLevel(level)
        logger.propagate = False  # avoids double output on the root logger

        # Rotating file handler (prevents unbounded log file growth)
        file_handler = RotatingFileHandler(
            log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        Logger._logger = logger

        Logger.info(f"Session started (PyInstaller: {hasattr(sys, '_MEIPASS')})")

    @staticmethod
    def _ensure_ready() -> Optional[logging.Logger]:
        if Logger._logger is None:
            # Logger.setup() was not called before use: do not log instead of
            # raising an exception. Print signal on stderr to avoid hiding the oversight.
            print("Logger.setup() was not called before use.", file=sys.stderr)
            return None
        return Logger._logger

    @staticmethod
    def info(message: str) -> None:
        logger = Logger._ensure_ready()
        if logger:
            logger.info(message)

    @staticmethod
    def warning(message: str) -> None:
        logger = Logger._ensure_ready()
        if logger:
            logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        logger = Logger._ensure_ready()
        if logger:
            logger.error(message)

    @staticmethod
    def exception(message: str = "Unhandled exception") -> None:
        """
        To be called only from within an except block: automatically captures
        the current stack trace via sys.exc_info().
        """
        logger = Logger._ensure_ready()
        if logger:
            logger.exception(message)

    @staticmethod
    def session_file_path() -> Optional[str]:
        """Returns the path to the current log file, or None if not initialized."""
        if Logger._log_dir is None:
            return None
        return os.path.join(Logger._log_dir, "gravityengine.log")
        