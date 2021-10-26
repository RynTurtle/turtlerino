def mrdestructoid(message):
    return ' '.join(format(ord(x), 'b') for x in message)
