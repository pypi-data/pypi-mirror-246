import logging

log = logging.getLogger(__name__)


def test_log():
    """Call some logging levels to test logging."""
    log.debug("debug")
    log.info("info")
    log.critical("critical")
    log.warning("warning")


test_log()
