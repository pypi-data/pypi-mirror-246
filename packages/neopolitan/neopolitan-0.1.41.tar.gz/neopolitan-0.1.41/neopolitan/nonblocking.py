"""Allows execution of board functions in a non-blocking manner"""

# pylint: disable=pointless-string-statement
# pylint: disable=wrong-import-position
"""
Manages interactions with the display board

See testboardrunner.py for an example:
    https://github.com/alyoshenka/neopolitan/blob/main/neopolitan/testboardrunner.py
"""
# pylint: disable=global-statement
import time
from threading import Thread
from queue import Queue
# pylint: disable=import-error
from neopolitan.neop import main as default
from neopolitan.demos import \
    display_all, \
    display_all_lowercase_letters, \
    display_all_uppercase_letters, \
    display_all_numbers, \
    display_all_symbols, \
    color_demo
from neopolitan.log import get_logger

# todo: is global var ok?
NEOPOLITAN_THREAD = None
EVENT_QUEUE = None

# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
def command_map(data):
    """Returns the appropriate function"""
    logger = get_logger()
    if data == 'open':
        logger.info('Returning "neopolitan open" func')
        return lambda : open_display(default)
    if data == 'close':
        logger.info('Returning "neopolitan close" func')
        return close_display
    if data == 'update':
        logger.info('Returning "neopolitan update" func')
        return update_display
    if data == 'test':
        logger.info('Returning "neopolitan test" func')
        return test_display
    if data == 'displayAll':
        logger.info('Returning "neopolitan displayAll" func')
        return lambda : open_display(display_all)
    if data == 'displayAllLowercase':
        logger.info('Returning "neopolitan displayAll" func')
        return lambda : open_display(display_all_lowercase_letters)
    if data == 'displayAllUppercase':
        logger.info('Returning "neopolitan displayAllUppercase" func')
        return lambda : open_display(display_all_uppercase_letters)
    if data == 'displayAllNumbers':
        logger.info('Returning "neopolitan displayAllNumbers" func')
        return lambda : open_display(display_all_numbers)
    if data == 'displayAllSymbols':
        logger.info('Returning "neopolitan displayAllSymbols" func')
        return lambda : open_display(display_all_symbols)
    if data == 'colorDemo':
        logger.info('Returning "neopolitan colorDemo" func')
        return lambda : open_display(color_demo)
    # todo: this should be somewhere else
    """
    if data == 'stockTicker':
        logger.info('Returning "neopolitan stockTicker" func')
        return lambda : open_display(default_tickers)
    # todo: this should be somewhere else
    if data == 'stockTickerSNP':
        logger.info('Returning "neopolitan stockTickerSNP" func')
        return lambda : open_display(snp_500)
        # todo: this should be somewhere else
    if data == 'stockTickerNASDAQ':
        logger.info('Returning "neopolitan stockTickerNASDAQ" func')
        return lambda : open_display(nasdaq_100)
    logger.warning('No Neopolitan action found for: %s', data)
    """
    return None

def open_display(func=default):
    """Open the neopolitan display with the default welcome message"""
    logger = get_logger()
    logger.info('running open_display with %s', func.__name__)

    global NEOPOLITAN_THREAD
    global EVENT_QUEUE
    if NEOPOLITAN_THREAD or EVENT_QUEUE:
        logger.warning('NEOPOLITAN_THREAD or EVENT_QUEUE already initialized,'\
                       ' but closing display anyway')
        close_display()

    EVENT_QUEUE = Queue()
    NEOPOLITAN_THREAD = Thread(target=func, args=(EVENT_QUEUE,))
    NEOPOLITAN_THREAD.start()

def close_display():
    """Close the neopolitan display"""
    logger = get_logger()
    logger.info('running close_display')

    global NEOPOLITAN_THREAD
    global EVENT_QUEUE

    if not (EVENT_QUEUE and NEOPOLITAN_THREAD):
        logger.warning('EVENT_QUEUE or NEOPOLITAN_THREAD not initialized')
        return

    EVENT_QUEUE.put('exit')

    NEOPOLITAN_THREAD.join()

    NEOPOLITAN_THREAD = None
    EVENT_QUEUE = None

def update_display(options):
    """Send arguments to the display"""
    logger = get_logger()
    logger.info('running update_display')

    def parse_option(opt):
        """Handles a single option"""
        value = options[opt]
        if not value:
            logger.warning('No value passed in %s', opt)
            return
        if not EVENT_QUEUE:
            logger.warning('Event queue not initialized yet')
            return

        logger.info('adding to queue: %s=%s', opt, value)
        # todo: check if string. need to?
        put_str = str(opt) + ' ' + str(value)
        EVENT_QUEUE.put(put_str)

    for opt in options:
        parse_option(opt)

def test_display():
    """Test that events can be passed"""
    logger = get_logger()
    logger.info('running test_display')

    def wait_then_add(slp, evt):
        """Sleep for time then add argument to queue"""
        logger.info('Waiting for %s s then putting %s', slp, evt)
        time.sleep(slp)
        EVENT_QUEUE.put(evt)
    def wait_then_do(slp, func):
        """Sleep for time then run function"""
        if not callable(func):
            logger.warning('Passed an uncallable: %s', func)
            return
        logger.info('Waiting for %s s then doing %s', slp, func.__name__)

        time.sleep(slp)
        func()

    open_display()
    Thread(target=wait_then_add, args=(5, 'say beepboop')).start()
    Thread(target=wait_then_do, args=(10, close_display)).start()
