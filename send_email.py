# import email
import smtplib
from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

def send_email(email, height, average_height, count):
    from_email = "*******@gmail.com"
    from_password = "*************"
    to_email = email

    subject = "Height data"
    message = "Hey there, your height is <strong>%s</strong>. Average height of all is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people." % (height, average_height, count)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(from_email, from_password)
    server.send_message(msg)
