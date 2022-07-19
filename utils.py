from datetime import datetime


def round_down(x, precision):
    return round(x - 5 * (10 ** (-precision - 1)), precision)


def get_local_timestamp():
    return str(datetime.now().timestamp())[0:10]
