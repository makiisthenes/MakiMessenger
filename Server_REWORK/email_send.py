import smtplib, datetime

# Yandex has a temp SPAM block, Gmail is the only working platform.
# EMAIL = "makimessenger@yandex.com"
EMAIL = "makimessenger@yahoo.com"
YAHOO_SMTP = "smtp.mail.yahoo.com"
PASSWORD = "chief.french.activity"
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
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (EMAIL, user, subj, timestamp, message)

    try:
        smtpObj = smtplib.SMTP(YAHOO_SMTP, 587)
        smtpObj.login(EMAIL, PASSWORD)
        smtpObj.sendmail(EMAIL, user, msg)
        print('[EMAIL]: Email has been sent, double check spam.')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)
        print("[Error]: Unable to send email.")