import os
import logging.config

import yaml


def setup_logging(
        default_path='./config/logging.yml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        log_dir_path = os.path.abspath("./logs")
        if not os.path.exists(log_dir_path):
            print("Logs directory does not find")
            os.mkdir(log_dir_path, 0o744)
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
