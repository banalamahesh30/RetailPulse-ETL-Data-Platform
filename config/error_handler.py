import traceback
from config.logger import logger


def handle_error(step_name, error):
    """
    Log details about an ETL pipeline error.
    """

    logger.error("=" * 70)
    logger.error(f"ETL STEP FAILED: {step_name}")
    logger.error(f"ERROR: {error}")
    logger.error("TRACEBACK:")
    logger.error(traceback.format_exc())
    logger.error("=" * 70)


def run_step(step_name, function):
    """
    Execute an ETL step with error handling.
    """

    logger.info("=" * 70)
    logger.info(f"STARTING: {step_name}")
    logger.info("=" * 70)

    try:
        result = function()

        logger.info(f"COMPLETED: {step_name}")

        return result

    except Exception as error:

        handle_error(step_name, error)

        raise