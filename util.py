from email_validator import validate_email


def email(_email):
    "This is going to be used in request parser arguments"
    if validate_email(_email, check_deliverability=False):
        return _email
