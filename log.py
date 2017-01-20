import logging

logger = logging.getLogger('rti')
#logger.setLevel(logging.CRITICAL)
#logger.setLevel(logging.ERROR)
#logger.setLevel(logging.WARNING)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s:%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


#def setup_rti_logger(name):
    #formatter = logging.Formatter(fmt='[%(asctime)-15s][%(levelname)s][%(module)s:%(funcName)s] %(message)s')
    #handler = logging.StreamHandler()
    #handler.setFormatter(formatter)
    #logger = logging.getLogger("name")
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(handler)

    #logger = logging.getLogger(name)
    #logger.setLevel(logging.ERROR)
    #FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s:%(name)s:%(funcName)s] %(message)s'
    #logging.basicConfig(format=FORMAT)

    #return logger


# OLD WAY
#import logging
#logger = logging.getLogger("Binary Codec")
#logger.setLevel(logging.ERROR)
#FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s:%(name)s:%(funcName)s] %(message)s'
#logging.basicConfig(format=FORMAT)