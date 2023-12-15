class CFDDNSError(Exception):
    """
    Base exception for cflare-ddns
    """

    pass


class ConfigInvalidError(CFDDNSError):
    """
    Raised when the config file is invalid
    """

    pass


class RecordUpdateError(CFDDNSError):
    """
    Raised when the new ip cannot be set
    """

    pass


class RecordNotFound(CFDDNSError):
    """
    Raised when a the A record cannot be fetched
    """

    pass


class PublicIPNotFound(CFDDNSError):
    """
    Raised when public ip cannot be fetched
    """

    pass
