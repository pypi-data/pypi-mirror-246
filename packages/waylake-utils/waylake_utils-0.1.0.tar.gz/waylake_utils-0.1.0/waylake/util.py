import logging.handlers
import os

def setup_logger(name, log_dir='logs'):
    # Determine the absolute path to the log directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_path, log_dir)

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Configure logging
    logger = logging.getLogger(name)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # File handler
    fileHandler = logging.FileHandler(os.path.join(log_path, f'{name}.log'))
    fileHandler.setFormatter(formatter)

    # Stream handler (for console output)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    return logger
