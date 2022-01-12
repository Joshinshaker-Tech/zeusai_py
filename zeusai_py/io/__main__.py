"""
When the IO module is run directly, it launches a basic interactive CLI client
.
The __main__ module also works as a good example of a simple client for other developers
to begin their plugins from.
"""
from zeusai_py import io
from zeusai_py.io import client
import getpass


def output(ai_out: str):
    """"""
    print(ai_out)


def main():
    host = input("ZeusAI Server Host (localhost):")
    port = int(input("ZeusAI Server Port (9387):"))

    # Default host and port
    if host is None:
        host = "127.0.0.1"
    if port is None:
        port = "9387"

    # Actual Client Code - Very simple to use.
    client_ = client.Client(host, port)

    # Authenticate
    username = input("Username: ")
    password = getpass.getpass()
    client_.authenticate(username, password)

    # Set the o
    client_.set_output_func(output)
    client_.recv_thread.start()
    while True:
        user_input = input("Input: ")
        client_.input(user_input)


if __name__ == "__main__":
    main()
