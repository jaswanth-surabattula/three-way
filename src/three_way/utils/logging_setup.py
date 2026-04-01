"""Logging configuration for Three-Way Arena.

Call ``setup_logging()`` once at startup (e.g. from ``launch()`` in ui/app.py).
After that, every module can do:

    import logging
    log = logging.getLogger(__name__)

Log levels:
  - Console: INFO  (high-level events — request sent, response received, errors)
  - File:    DEBUG (everything — raw token counts, latency, full error tracebacks)

Log file location: ``logs/three_way.log`` relative to the current working
directory (i.e. the project root when launched with ``uv run three-way``).
The file rotates at 5 MB and keeps the last 3 backups.
"""

import logging
import logging.handlers
from pathlib import Path


_CONFIGURED = False  # guard against calling setup_logging() more than once


def setup_logging(log_dir: str = "logs") -> None:
    """Configure root logger with a console handler (INFO) and rotating file handler (DEBUG).

    Safe to call multiple times — only configures on the first call.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURED = True

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / "three_way.log"

    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — DEBUG, rotates at 5 MB, keeps 3 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # Console handler — INFO only (don't flood the terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.addHandler(console_handler)

    logging.getLogger(__name__).info("Logging initialised — writing to %s", log_file)
