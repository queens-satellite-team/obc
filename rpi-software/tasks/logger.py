# Imports
import os
import sys
import logging

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

class SatelliteLogger:
    '''Custom logger to be shared across all satellite systems.'''

    _LOG = None

    @staticmethod
    def __create_logger(module_name, console_log_output, console_log_level, console_log_color,
                        logfile_file, logfile_log_level, logfile_log_color, log_line_template):
        """
        A private method that interacts with the python
        logging module.
        """

        # Initialize the class variable with logger object
        SatelliteLogger._LOG = logging.getLogger(module_name)

        # Set global log level to 'debug' (required for handler levels to work)
        SatelliteLogger._LOG.setLevel(logging.DEBUG)

        # Create console handler
        console_log_output = console_log_output.lower()
        if (console_log_output == "stdout"):
            console_log_output = sys.stdout
        elif (console_log_output == "stderr"):
            console_log_output = sys.stderr
        else:
            print("Failed to set console output: invalid output: '%s'" % console_log_output)
            return False
        console_handler = logging.StreamHandler(console_log_output)

        # Set console log level
        try:
            console_handler.setLevel(console_log_level.upper()) # only accepts uppercase level names
        except:
            print("Failed to set console log level: invalid level: '%s'" % console_log_level)
            return False

        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color)
        console_handler.setFormatter(console_formatter)
        SatelliteLogger._LOG.addHandler(console_handler)

        # Create log file handler
        try:
            logfile_handler = logging.FileHandler(logfile_file)
        except Exception as exception:
            print("Failed to set up log file: %s" % str(exception))
            return False

        # Set log file log level
        try:
            logfile_handler.setLevel(logfile_log_level.upper()) # only accepts uppercase level names
        except:
            print("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
            return False

        # Create and set formatter, add log file handler to logger
        logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
        logfile_handler.setFormatter(logfile_formatter)
        SatelliteLogger._LOG.addHandler(logfile_handler)

        return SatelliteLogger._LOG

    @staticmethod
    def get_logger(module_name, console_log_output="stdout", console_log_level="debug", console_log_color=True,
                    logfile_file="logger.log", logfile_log_level="info", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(name)s] [%(levelname)-8s] %(message)s%(color_off)s"):
        """
        A static method called by other modules to initialize
        logger in their own module.
        """

        logger = SatelliteLogger.__create_logger(module_name, console_log_output, console_log_level, console_log_color,
                                    logfile_file, logfile_log_level, logfile_log_color, log_line_template)
        # return the logger object
        return logger

# Main function
def main():

    # Setup logging
    logger_file_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.log'
    custom_logger = SatelliteLogger.get_logger(logger_file_name)
    if (not custom_logger):
        print("Failed to setup logging, aborting.")
        return 1

    # Log some messages
    custom_logger.debug("Debug message")
    custom_logger.info("Info message")
    custom_logger.warning("Warning message")
    custom_logger.error("Error message")
    custom_logger.critical("Critical message")

# Call main function
if (__name__ == "__main__"):
    sys.exit(main())