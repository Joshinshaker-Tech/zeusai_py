"""
When the IO module is run directly, it launches a basic interactive CLI client.

The __main__ module also works as a good example of a simple client for other developers
to begin their plugins from.
"""
from . import client
import getpass


def output(ai_out: str):
    """"""
    print(ai_out)


def main() -> None:
    host = input("ZeusAI Server Host (localhost):")
    port = input("ZeusAI Server Port (9387):")

    # Default host and port
    if not host:
        host = "127.0.0.1"
    if not port:
        port = "9387"
    port = int(port)

    # Actual Client Code - Very simple to use.
    client_ = client.Client(host, port)

    # Authenticate
    username = input("Username: ")
    password = getpass.getpass()
    client_.set_output_func(output)
    client_.authenticate(username, password)

    while True:
        user_input = input("Input: ")
        client_.input(user_input)


if __name__ == "__main__":
    main()
