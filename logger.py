from abc import abstractmethod
from datetime import datetime, timedelta
import json
import logging
import pytz
import random
import re
import requests
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Protocol(Enum):
    """
    Enum class to represent valid protocols.
    """
    TCP = "TCP"
    UDP = "UDP"

class SyslogFormat(Enum):
    """
    Enum class to represent valid syslog formats.
    """
    CEF = "CEF"

class HttpFormat(Enum):
    """
    Enum class to represent valid http data formats
    """
    JSON = "JSON"

class Logger:
    """
    A base class to represent a logger that stores data in a dictionary of strings mapped to arrays.
    """

    def __init__(self):
        """
        Initializes the Logger object with an empty dictionary for fields.
        """
        self._fields = {}

    @property
    def fields(self):
        """
        Returns the dictionary of fields.

        Returns:
            dict: The dictionary of fields.
        """
        return self._fields
    
    @fields.setter
    def fields(self, value: dict):
        """
        Sets the fields.

        Args:
            value (dict): the fields.
        """
        self._fields = value
        

    @abstractmethod
    def send_log(self):
        """
        An abstract method that should be implemented by subclasses to send the log.
        """

class SyslogLogger(Logger):
    """
    A class to represent a logger specifically for syslog messages.
    """
    def __init__(self):
        """
        Initializes the SyslogLogger object.
        """
        super().__init__()
        self._destination_ip = None
        self._port = None
        self._protocol = None
        self._format = None

    @property
    def destination_ip(self):
        """
        Returns the destination IP address.

        Returns:
            str: The destination IP address.
        """
        return self._destination_ip

    @destination_ip.setter
    def destination_ip(self, value: str):
        """
        Sets the destination IP address after validating it is a valid IPv4 address.

        Args:
            value (str): The destination IP address.

        Raises:
            ValueError: If the provided value is not a valid IPv4 address.
        """
        if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", value):
            raise ValueError(f"Invalid IPv4 address: {value}")
        self._destination_ip = value

    @property
    def port(self):
        """
        Returns the port number.

        Returns:
            int: The port number.
        """
        return self._port

    @port.setter
    def port(self, value: int):
        """
        Sets the port number after validating it is within the valid range (1-65535).

        Args:
            value (int): The port number.

        Raises:
            ValueError: If the provided value is not a valid port number.
        """
        if not 1 <= value <= 65535:
            raise ValueError(f"Invalid port number: {value}. Must be between 1 and 65535.")
        self._port = value

    @property
    def protocol(self):
        """
        Returns the protocol.

        Returns:
            Protocol: The protocol.
        """
        return self._protocol

    @protocol.setter
    def protocol(self, value: Protocol):
        """
        Sets the protocol.

        Args:
            value (Protocol): The protocol.

        Raises:
            ValueError: If the provided value is not a valid Protocol enum member.
        """
        if value not in Protocol:
            raise ValueError(f"Invalid protocol: {value}. Must be one of {list(Protocol)}.")
        self._protocol = value

    @property
    def format(self):
        """
        Returns the format.

        Returns:
            Format: The format.
        """
        return self._format

    @format.setter
    def format(self, value: SyslogFormat):
        """
        Sets the format.

        Args:
            value (Format): The format.

        Raises:
            ValueError: If the provided value is not a valid Format enum member.
        """
        if value not in SyslogFormat:
            raise ValueError(f"Invalid format: {value}. Must be one of {list(SyslogFormat)}.")
        self._format = value

class HttpLogger(Logger):
    """
    A class to represent a logger specifically for HTTP logs.
    """
    def __init__(self):
        """
        Initializes the HttpLogger object.
        """
        super().__init__()
        self._url = None
        self._send_format = HttpFormat.JSON
        self._api_key = None

    @property
    def url(self):
        """
        Returns the URL.

        Returns:
            str: The URL.
        """
        return self._url

    @url.setter
    def url(self, value: str):
        """
        Sets the URL.

        Args:
            value (str): The URL.
        """
        self._url = value

    @property
    def send_format(self):
        """
        Returns the send format.

        Returns:
            SendFormat: The send format.
        """
        return self._send_format
    
    @send_format.setter
    def send_format(self, value: HttpFormat):
        """
        Sets the format.

        Args:
            value (Format): The format.

        Raises:
            ValueError: If the provided value is not a valid Format enum member.
        """
        if value not in HttpFormat:
            raise ValueError(f"Invalid format: {value}. Must be one of {list(HttpFormat)}.")
        self._format = value

    @property
    def api_key(self):
        """
        Returns the API key.

        Returns:
            str: The API key.
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        """
        Sets the API key.

        Args:
            value (str): The API key.
        """
        self._api_key = value

    def send_log(self):
        """
        Sends the log message via HTTP.
        """
        if self.url is None or self.api_key is None:
            raise ValueError("URL and API key must be set before sending a log.")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }

        log = {}

        logging.debug(self.fields)

        for k, v in self.fields.items():
            if k == 'timestamp_format':
                log['timestamp'] = (datetime.now(pytz.utc) + timedelta(0,-3)).strftime(v)
            else:
                log[k] = random.choice(v)
        
        try:
            logging.debug(f"Sending log message: {log}")
            response = requests.post(self.url, headers=headers, data=json.dumps(log))
            response.raise_for_status()  # Raise an exception for bad status codes
            logging.debug("Log sent successfully!")
        except requests.exceptions.RequestException as e:
            logging.exception(f"An error occurred while sending the log: {e}")