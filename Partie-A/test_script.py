def crash_if_too_long(s):
    if len(s) > 9:
        raise ValueError
