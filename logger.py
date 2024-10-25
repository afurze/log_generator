import re
from enum import Enum

class Protocol(Enum):
    """
    Enum class to represent valid protocols.
    """
    TCP = "TCP"
    UDP = "UDP"

class Format(Enum):
    """
    Enum class to represent valid formats.
    """
    CEF = "CEF"

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
    def format(self, value: Format):
        """
        Sets the format.

        Args:
            value (Format): The format.

        Raises:
            ValueError: If the provided value is not a valid Format enum member.
        """
        if value not in Format:
            raise ValueError(f"Invalid format: {value}. Must be one of {list(Format)}.")
        self._format = value