import logging
class Logging:

    def __init__(self,logger,formatter,file_handler):
        logger = logging.getLogger()
        self.logger=logger
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        self.formatter=formatter
        file_handler = logging.FileHandler('logs.log')
        self.file_handler=file_handler

        logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # logger.basicConfig()
    # logger.getLogger().setLevel(logging.DEBUG)
    # logger.getLogger('foo').debug('message')
    # logger.getLogger().setLevel(logging.INFO)
    # logger.getLogger('foo').debug('message')
        logger.log(logging.WARNING,"xnj ===d wdawd wa dawdaw")