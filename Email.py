import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_code(user_email):    
    try:
        sender_email = "noreply.socialnetworkapp@gmail.com"
        sender_password = "mmfg chsp hbhz hhav"
    
        # generate random 4-digit verification code
        verification_code = random.randint(1000, 9999) 
    
        # set up SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
    
        # construct email message
        subject = "Verification Code"
        body = f"Your verification code is: {verification_code}"
        msg = MIMEMultipart()  
        msg['From'] = 'Degree Finder <noreply.socialnetworkapp@gmail.com>'
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
    
        # send the email
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
        return verification_code

    except Exception as e:
        st.error(f"Failed to send verification code: {e}")
        return none


