# por razões de autenticao, é necessário usar o seguinte sender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, sys
import socket


# por razões de autenticao, é necessário usar o seguinte sender
sender = "Ace 2023 <pm.ace2022.noreply@gmail.com>"

def send_confirm_mail(receiver_name, 
             receiver_email, 
             vacine_name, 
             vacine_date, 
             vacine_time, 
             vacine_location): 
    
    receiver = receiver_name + " <"+ receiver_email + ">"

    body = "Caro " + receiver_name + ",\n\n" + "O seu agendamento da vacina " + vacine_name + " encontra-se confirmado para a data " + vacine_date + " às "\
        + vacine_time + " no centro de vacinação " + vacine_location + ".\n\n" + "Com os melhores cumprimentos,\n" + "Equipa Get-a-Vax"
    
    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'a subject'

    #message.attach(MIMEText(body, 'html'))
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("marechal.int.ace.premium-minds.com", timeout=10) as session:
            session.sendmail(sender, receiver, message.as_string())
            session.quit()
    except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError, socket.timeout) as e:
        print("Failed to send email:", str(e))

    return

