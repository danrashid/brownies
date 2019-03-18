from base64 import b64encode


def base64(string):
    return (b64encode(string.encode())).decode()
