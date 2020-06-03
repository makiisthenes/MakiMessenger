# from validate_email import validate_email  - ommited
from email_validator import validate_email, EmailNotValidError
from twofactor import verify_user

'''
def email_val(user):
    print("Please wait while we verify your email...")
    is_valid = validate_email(user, verify=True)
    if is_valid:
        verify_user(user)
        return True
    else:
        return False

email_val("michaelperes1@gmail.com")
'''


def email_val(user):
    try:
        print("Please wait while we validate email...")
        valid = validate_email(user)
        email = valid.email
        verify_user(user)
        print("This email is valid :)")
        return True
    except EmailNotValidError as e:
        print(str(e))
        return e

