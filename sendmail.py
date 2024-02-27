from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, sys

# por razões de autenticao, é necessário usar o seguinte sender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, sys

# por razões de autenticao, é necessário usar o seguinte sender
sender = "Ace 2023 <pm.ace2022.noreply@gmail.com>"
receiver = "Diego Maradona <diogojpaMaradona@dispostable.com>"


body = "O seu agendamento da vacina <Nome Vacina> encontra-se confirmado para a data <Data e Hora da Vacina> no centro de vacinação <Nome Centro>."

message = MIMEMultipart('alternative')
message['From'] = sender
message['To'] = receiver
message['Subject'] = 'a subject'

#message.attach(MIMEText(body, 'html'))
message.attach(MIMEText(body, 'plain'))


session = smtplib.SMTP("marechal.int.ace.premium-minds.com")
session.sendmail(sender, receiver, message.as_string())
session.quit()
sys.exit(0)

