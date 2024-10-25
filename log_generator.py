from asyncio import sleep
import logging
from logger import HttpLogger, HttpFormat, SyslogLogger, SyslogFormat, Protocol
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
    try:
        config = read_yaml('format.yaml')
        loggers_config = config['loggers']

        log_send_count = config['general']['logs_to_send']
        delay = config['general']['delay']

        loggers = []

        for k, v in loggers_config.items():
            if v['collector_type'].upper() == "HTTP":
                logger = HttpLogger()
                logger.api_key = v['API_KEY']
                logger.send_format = HttpFormat.JSON
                logger.url = v['url']
            elif v['collector_type'].upper() == "SYSLOG":
                logger = SyslogLogger()
                logger.destination_ip = v['destination_ip']
                logger.port = v['destination_port']
                if v['protocol'].upper() == "UDP":
                    logger.protocol = Protocol.UDP
                elif v['protocol'].upper() == "TCP":
                    logger.protocol = Protocol.TCP
                else:
                    logging.exception(f"Invalid protocol {v['protocol']}. Must be one of {list(Protocol)}.")

                if v['send_format'].upper() == "CEF":
                    logger.format = SyslogFormat.CEF
                elif v['send_format'].upper() == "LEEF":
                    logger.format = SyslogFormat.LEEF
                else:
                    logging.exception(f"Invalid format {v['send_format']}. Must be one of {list(SyslogFormat)}.")
            
            logger.fields['timestamp_format'] = v['timestamp_format']
            logger.fields = v['fields']
            loggers.append(logger)

        for i in range(0, log_send_count):
            for l in loggers:
                l.send_log()
            sleep(delay)
    
    except Exception as e:
        logging.exception(e)

if __name__ == "__main__":
    main()