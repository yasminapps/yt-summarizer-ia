# utils/decorators.py
import time
import functools
from utils.logger import get_logger
from functools import wraps

logger = get_logger()

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.debug(f"⏱️ Function `{func.__name__}` executed in {duration:.2f}s")

        # Injecte execution_time si résultat est dict
        if isinstance(result, dict):
            result["execution_time"] = round(duration, 2)

        return result
    return wrapper

def safe_exec(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"❌ Exception in `{func.__name__}`: {e}")
            raise e
    return wrapper

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"🚀 Entering function: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"✅ Successfully executed: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"❌ Error in {func.__name__}: {e}")
            raise  # on relance l'exception pour ne pas la cacher
    return wrapper
