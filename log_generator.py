from asyncio import sleep
import logging
from logger import HttpLogger, HttpFormat
import yaml


# Configure logging
logging.basicConfig(level=logging.DEBUG)

def read_yaml(conf_file):
    with open(conf_file, 'r') as stream:
        try:
            loaded = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    return loaded
            

def main():
    config = read_yaml('format.yaml')
    loggers_config = config['loggers']

    log_send_count = config['general']['logs_to_send']
    delay = config['general']['delay']

    loggers = []

    for k, v in loggers_config.items():
        if v['collector_type'] == "HTTP":
            logger = HttpLogger()
            logger.fields = v['fields']
            logger.api_key = v['API_KEY']
            logger.send_format = HttpFormat.JSON
            logger.url = v['url']
            logger.fields['timestamp_format'] = v['timestamp_format']

            loggers.append(logger)

    for i in range(0, log_send_count):
        for l in loggers:
            l.send_log()
        sleep(delay)

if __name__ == "__main__":
    main()