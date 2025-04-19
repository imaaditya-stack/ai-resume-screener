import logging
import time
from pipeline.state_managers.global_state_manager import GlobalStateManager
import json

# Basic configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def logger(func):
    """
    Decorator that adds logging functionality to pipeline stage methods.
    Logs start/completion times, duration, and output for each stage.
    Handles errors and provides detailed logging of exceptions.
    """

    def wrapper(self, state, global_state: GlobalStateManager = None):
        # Get logger instance for this class
        logger = logging.getLogger(self.__class__.__name__)

        start_time = time.time()
        # logger.info(f"Starting stage: {self.__class__.__name__}")

        try:
            # Execute the decorated function
            state, output_from_stage = func(self, state, global_state)

            # Calculate and log duration
            end_time = time.time()
            duration = end_time - start_time

            # Log the output appropriately based on type
            if isinstance(output_from_stage, dict):
                logger.info(f"Stage output from {self.__class__.__name__}\n")
                logger.info(json.dumps(output_from_stage, indent=2))
            elif output_from_stage is not None:
                logger.info(f"Stage output from {self.__class__.__name__}\n")
                logger.info(output_from_stage)

            logger.info(
                f"Completed stage: {self.__class__.__name__} in {duration:.2f}s"
            )

            return state, output_from_stage

        except Exception as e:
            # Log detailed error information
            logger.info(
                f"Error in stage {self.__class__.__name__}: {str(e)}"
                # exc_info=True,
                # stack_info=True,
            )
            raise e

    return wrapper
