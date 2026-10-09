from hashlib import md5


def hashpassword(password):
    hash = md5(password.encode('utf8')).hexdigest()
    return hash
