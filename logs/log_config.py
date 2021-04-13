
log_config = {
    'version': 1,
    'formatters': {
        'reply_formatter': {
            'format': '[%(asctime)s]: %(levelname)s %(message)s',
        },
        'main_formatter': {
            'format': '[%(asctime)s]: %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'reply_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'reply_formatter',
            'filename': 'logs/reply.log',
            'encoding': 'UTF-8',
        },
        'main_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'main_formatter',
            'filename': 'logs/main.log',
            'encoding': 'UTF-8',
        },
    },
    'loggers': {
        'reply': {
            'handlers': ['reply_handler', 'main_handler'],
            'level': 'DEBUG',
        },
        'main': {
            'handlers': ['main_handler'],
            'level': 'DEBUG',
        },
    },
}
