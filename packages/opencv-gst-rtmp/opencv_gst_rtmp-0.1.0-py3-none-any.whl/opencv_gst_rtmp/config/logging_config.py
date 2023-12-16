import logging.config
from opencv_gst_rtmp.config.config import Config
config = Config()
logging_schema = {
    # Always 1. Schema versioning may be added in a future release of logging
    "version": 1,
    # "Name of formatter" : {Formatter Config Dict}
    "formatters": {
        # Formatter Name
        "standard": {
            # class is always "logging.Formatter"
            "class": "logging.Formatter",
            # Optional: logging output format
            "format": "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        }
    },
    # Handlers use the formatter names declared above
    "handlers": {
        # Name of handler
        "console": {
            # The class of logger. A mixture of logging.config.dictConfig() and
            # logger class-specific keyword arguments (kwargs) are passed in here. 
            "class": "logging.StreamHandler",
            # This is the formatter name declared above
            "formatter": "standard",
            # The default is stderr
            # "stream": "ext://sys.stdout"
        }
    },
    "root" : {
        "level": f"{config.OPENCV_GST_RTMP_LOG_LEVEL}",
        "handlers": ["console"],
        "propagate": False
    }
}

logging.config.dictConfig(logging_schema)