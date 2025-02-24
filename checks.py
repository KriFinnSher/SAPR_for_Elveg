import re

def ch1(val):
    pattern = r'^([1-9]\d*|)$'
    return re.match(pattern, val) is not None


def ch2(val):
    pattern = r'^(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def ch3(val):
    pattern = r'^-?(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None