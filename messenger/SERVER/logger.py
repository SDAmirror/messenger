import logging
class Logging:

    def __init__(self,logger=None,formatter=None,file_handler=None):
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
    #     logger.log(logging.WARNING,"xnj ===d wdawd wa dawdaw")
# =======
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
#
#     file_handler = logging.FileHandler('logs.log')
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
# >>>>>>> a920df38902ff09f1d2ca38f1196a02618f45f81
