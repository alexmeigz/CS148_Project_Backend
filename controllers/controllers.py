def verify(args, params):
    for arg in args:
        if args not in params:
            return False
    return True

