class IOException:
    """
    The Base exception for all IO module related exceptions
    """
    pass


class InvalidEndpoint(IOException):
    """
    The client attempted to access a non-existent endpoint is invalid.
    """
    pass


class InvalidParams(IOException):
    """
    The params provided to an endpoint are incorrect. This may be that they are the wrong
    params for the endpoint called, or that they have the wrong type.
    """
    pass


class InvalidJSON(IOException):
    """
    The request received by the server is not in a valid JSON format.
    """
    pass


class Forbidden(IOException):
    """
    The client did not authenticate with the server before calling
    a secure endpoint.
    """
    pass


class AuthTimeout(IOException):
    """
    The client failed to successfully authenticate in the allotted number
    of attempts. This is a fatal exception and the connection will be closed
    after it is raised.
    """
    pass


class AuthFailed(IOException):
    """
    The username and/or password provided to the authentication endpoint
    are incorrect.
    """
    pass


# Source: https://github.com/python/cpython/blob/3.7/Lib/asyncio/streams.py
class IncompleteReadError(EOFError):
    """
    Incomplete read error.
    """
    def __init__(self, partial, expected):
        super().__init__(f'{len(partial)} bytes read on a total of '
                         f'{expected!r} expected bytes')
        self.partial = partial
        self.expected = expected

    def __reduce__(self):
        return type(self), (self.partial, self.expected)
