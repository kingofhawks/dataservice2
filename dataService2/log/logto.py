# coding=utf-8
# import os
# import sys
# sys.path.append(os.getcwd() + '/../')
import logging

def logTo(loggerName, level, message):
    logger = logging.getLogger(loggerName)

    if(level == 'info'):
        logger.info(message)
    if(level == 'warning'):
        logger.warning(message)
    if(level == 'INFO'):
        logger.info(message)
    if(level == 'INFO'):
        logger.info(message)
    if(level == 'INFO'):
        logger.info(message)
    
    
def logtoDebug(loggerName, message):
    logger = logging.getLogger(loggerName)
    logger.info(message)
    
def logtoInfo(loggerName, message):
    logger = logging.getLogger(loggerName)
    logger.info(message)

def logtoWarning(loggerName, message):
    logger = logging.getLogger(loggerName)
    logger.info(message)

def logtoError(loggerName, message):
    logger = logging.getLogger(loggerName)
    logger.info(message)

def logtoCritical(loggerName, message):
    logger = logging.getLogger(loggerName)
    logger.info(message)
#
#
#
#
#
