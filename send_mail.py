import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

def sendMail(receiver_email, time, date):
    FIXED_TIME = (datetime.today() + timedelta(minutes=time)).strftime('%H:%M')
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "support@passcam.cm" #"ndoprime@gmail.com"
    message = "test"
    password = "^H0zxo53" #"qzlffcpicscwlopm"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Alert UPS : "+str(time)+" minutes restantes avant extinction"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
    <body>
        <p>
            <h4>Alert UPS : <span style='color:red; font-family: bold'>"""+str(time)+""" minutes</span> restantes avant extinction</h4><br>
            Heure de passage en mode batterie : """+date+"""<br>
            Heure prévue pour l'extinction : """+FIXED_TIME+"""
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("chiron.ch-dns.net", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        
# sendMail("samy.ndo@augentic.com", 2, "test")