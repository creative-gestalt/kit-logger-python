import logging
import os.path

logger = logging.getLogger()


def begin_log(user, zip_code):
    file = os.path.join('./user_member_numbers/%s/ALL/logs/%s-log.txt' % (user, zip_code))
    logging.basicConfig(filename=file,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info('********************** kit-logger history **********************')
    logger.handlers = [logging.FileHandler(file)]  # this skips root logging since there is a handler
    logger.propagate = False


def message(text):
    logger.info(text)


def shutdown():
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
