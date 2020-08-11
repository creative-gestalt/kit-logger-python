import logging


log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('./data/temp/kt.log')
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(log_formatter)
# root_logger.addHandler(console_handler)


def print_and_log(message):
    root_logger.info(message)
    print(message)
