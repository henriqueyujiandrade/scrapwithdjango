import smtplib
import email.message

import os

import dotenv

dotenv.load_dotenv()

class Email:
    def send_email(monitor,value, link):
        email_body = f"""
        <p>Olá!!!</p>

        <p>O {monitor}</p>

        <p>O valor é R${value}</p>

        <p>Segue o link para compra:</p>
        <p>{link}</p>

        <p>att,</p>
        <p>Henrique Andrade</p>
        <p>HayaDev Scrapping Bot</p>
        """
        msg = email.message.Message()
        msg['Subject'] = "Monitor Gamer Abaixo de R$900!"
        msg['From'] = os.getenv("MY_GMAIL")
        msg['To'] = os.getenv("EMAIL_TO_SEND")
        password = os.getenv("MY_GMAIL_APP_PASSWORD")
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_body)
        
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        s.login(msg['From'], password)
        s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))

        return True