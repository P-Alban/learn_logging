import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

old_factory = logging.getLogRecordFactory()


# create new factory for logging record
def create_new_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.upper_case = record.getMessage().upper()
    record.getMessage = lambda: record.upper_case
    return record


logging.setLogRecordFactory(create_new_factory)


# custom handler
class CustomHandler(logging.Handler):

    def emit(self, record):  # some stupid logic
        record = super(CustomHandler, self).format(record)
        with open("custom_file.txt", "w") as fp:
            fp.write(record)


# custom filter
class CustomFilter(logging.Filter):

    def filter(self, record):
        return record.getMessage().startswith('H')


file_handler = logging.FileHandler(filename="log.txt", mode="w")
console_handler = logging.StreamHandler()

file_formatter = logging.Formatter(fmt="{levelname} - ON LINE {lineno} - {asctime} - {message}", style='{')

file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.ERROR)

console_handler.setFormatter(file_formatter)

custom_handler = CustomHandler()
custom_handler.setFormatter(file_formatter)
custom_handler.addFilter(CustomFilter())
custom_handler.setLevel(logging.CRITICAL)


logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(custom_handler)


logger.error("Some error happened")
logger.debug("Some debug message")
logger.critical("Critical message")
logger.critical("Hello critical message")
