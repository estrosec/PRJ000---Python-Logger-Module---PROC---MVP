import logger
from src.logger import LOG_LEVEL_LOW, LOG_LEVEL_MEDIUM, LOG_LEVEL_HIGH, LOG_LEVEL_ALL


def main():
    log = logger.create_logger("MyLogger")
    logger.initialize_logger(log, True, True)
    log2 = logger.create_logger("MyLogger 2")
    logger.initialize_logger(log2, True, True)

    logger.set_log_level(log2, LOG_LEVEL_LOW)

    logger.fatal(log, "Testing Fatal Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.error(log, "Testing Error Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.warning(log, "Testing Warning Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.success(log, "Testing Success Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.information(log, "Testing Information Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.debug(log, "Testing Debug Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.trace(log, "Testing Trace Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))

    logger.fatal(log2, "Testing Fatal Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.error(log2, "Testing Error Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.warning(log2, "Testing Warning Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.success(log2, "Testing Success Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.information(log2, "Testing Information Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.debug(log2, "Testing Debug Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))
    logger.trace(log2, "Testing Trace Log Message %s %d %f" % ("Testing String Concat", 5, 5.5))


if __name__ == "__main__":
    main()