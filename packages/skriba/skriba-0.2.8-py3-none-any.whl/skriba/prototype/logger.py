import os
import inspect
import skriba.prototype.console

PREVIOUS_FUNCTION = 1
PENULTIMATE_FUNCTION = 2


def _add_verbose_info(message: str, color: str = "blue") -> str:
    function_name = inspect.stack()[PENULTIMATE_FUNCTION].function
    return (
        "[ [{color}]{function_name}[/] ]: {message}".format(
            function_name=function_name,
            message=message,
            color=color
        ))


def info(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    message = _add_verbose_info(message=message, color="blue")

    logger = skriba.prototype.console.get_logger(logger_name=logger_name)
    logger.info(message, extra={"markup": markup})


def debug(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="green")

    logger = skriba.prototype.console.get_logger(logger_name=logger_name)
    logger.debug(message, extra={"markup": markup})


def warning(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    message = _add_verbose_info(message=message, color="yellow")
    logger = skriba.prototype.console.get_logger(logger_name=logger_name)
    logger.warning(message, extra={"markup": markup})


def critical(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    message = _add_verbose_info(message=message, color="bold red blink")
    logger = skriba.prototype.console.get_logger(logger_name=logger_name)
    logger.critical(message, extra={"markup": markup})


def error(message, markup=True, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    message = _add_verbose_info(message=message, color="blink red")
    logger = skriba.prototype.console.get_logger(logger_name=logger_name)
    logger.error(message, extra={"markup": markup})
