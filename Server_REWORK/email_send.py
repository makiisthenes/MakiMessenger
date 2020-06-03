import smtplib, datetime

# Yandex has a temp SPAM block, Gmail is the only working platform.
# EMAIL = "makimessenger@yandex.com"
YAHOO_EMAIL = "makimessenger@yahoo.com"
GMAIL_EMAIL = "markiring1988@gmail.com"
YAHOO_SMTP = "smtp.mail.yahoo.com"
PASSWORD = "Password"
YANDEX_SMTP = "smtp.yandex.com"
GMAIL_SMTP = "smtp.gmail.com"

def send_f2a(user, code):
    date_object = datetime.date.today()
    timestamp = datetime.datetime.strptime(str(date_object), "%Y-%m-%d").strftime("%d/%m/%Y")
    subj = "F2A Code - Maki Messenger"
    message = f"""
    Use this F2A Code in MakiMessenger to validate account.
    Your code is: {code}
    Thanks,
    MakiMessenger
    """
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (GMAIL_EMAIL, user, subj, timestamp, message)

    try:
        smtpObj = smtplib.SMTP(GMAIL_SMTP, 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(GMAIL_EMAIL, PASSWORD)
        smtpObj.sendmail(GMAIL_EMAIL, user, msg)
        print('[EMAIL]: Email has been sent, double check spam.')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)
        print("[Error]: Unable to send email.")
