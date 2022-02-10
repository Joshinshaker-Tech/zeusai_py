import socket
import json
import threading
from zeusai_py.io import _socket_io
from zeusai_py.io import exceptions


class Client:
    """ This class handles connecting to and interacting with the ZeusAI server's
    I/O API.

    Instantiating this class connects to the ZeusAI server specified in args automatically.

    :param host: String containing the hostname the ZeusAI Server is listening on.
    :param port: Int containing the port the ZeusAI server is listening on.
    :return: None
    """
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        self.reader = _socket_io.SocketStreamReader(self.conn)
        self.output_func = None
        self.recv_thread = threading.Thread(target=self._recv_loop)

    def authenticate(self, username: str, password: str) -> None:
        """ Authenticates with the ZeusAI server.

        This must be called BEFORE any other requests are made.

        :param username: The username to use for authentication with the server
        :param password: The password to use for authentication with the server
        :return: None
        """
        # TODO - Figure out how to deal with authentication errors.
        request_dict = {"endpoint": "auth", "params": {"user": username, "pass": password}}
        self._send_request(request_dict)

    def input(self, input_: str) -> None:
        """ Provide an input from the user for the AI to process and respond to.

        :param input_: String containing the user's input.
        :return: None
        """
        request_dict = {"endpoint": "input", "params": input_}
        self._send_request(request_dict)

    def set_output_func(self, func) -> None:
        """ Sets the function which is called when the server wants to send a message to the user.

        :param func: a function to be called by the recv_thread when the AI provides an output to the user.
            Should take a param for a string containing the AI output.
        :return: None
        """
        self.output_func = func

    def _get_response(self) -> dict:
        response = self.reader.readline()
        response = json.loads(response)
        return response

    def _send_request(self, request_dict: dict) -> None:
        """ Serializes request_dict into a JSON bytes object and sends it to the server.

        :param request_dict: Dictionary containing a valid request for the ZeusAI Server API
        :return: None
        """
        serialized_json = json.dumps(request_dict) + "\n"
        serialized_json = serialized_json.encode("utf8")
        self.conn.sendall(serialized_json)

    def _recv_loop(self) -> None:
        """ Loop which runs in a thread to get output from the AI server.
        Takes a set of functions which are called when the associated endpoint is called."""
        while True:
            response = self._get_response()
            if response["endpoint"] == "output":
                self.output_func(response["params"])
            elif response["endpoint"] == "error":
                original_request = response["params"]["original_request"]
                error = response["params"]["error"]
                if error == "invalid endpoint":
                    raise exceptions.InvalidEndpoint(f"The endpoint in request {original_request} is invalid")
                elif error == "invalid params":
                    raise exceptions.InvalidParams(f"The params included in request {original_request} are invalid")
                elif error == "invalid json":
                    raise exceptions.InvalidJSON(f"The server returned an invalid JSON error because a request was not sent in the form of a valid JSON.")
                elif error == "not implemented":
                    pass
                elif error == "forbidden":
                    raise exceptions.Forbidden(f"")
                    # TODO - write a message
                elif error == "auth timeout":
                    raise exceptions.AuthTimeout(f"")
                    # TODO - write a message
