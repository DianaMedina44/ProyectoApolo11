import hashlib

def generate_hash(*args):
    """
    This function generates a hash with the information provided by the user.
    """

    string_to_hash = ""

    for arg in args:
        string_to_hash += str(arg)

    hashed_string = hashlib.sha256(string_to_hash.encode()).hexdigest()

    return hashed_string
   