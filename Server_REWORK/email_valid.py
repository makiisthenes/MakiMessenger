from validate_email import validate_email
from twofactor import verify_user

def email_val(user):
    is_valid = validate_email(user, verify=True)
    if is_valid:
        verify_user(user)
        return True
    else:
        return False