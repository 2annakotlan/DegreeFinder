import smtplib
import random
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_verification_code(user_email):
    sender_email = "noreply.socialnetworkapp@gmail.com"
    # Get email password from environment variables for security
    sender_password = os.getenv("EMAIL_PASSWORD")  # Store the password securely in an environment variable
    
    # Verification code
    verification_code = random.randint(1000, 9999)  # Random 4 digit verification code 
    
    try:
        # SMTP server setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Email message setup
        subject = "Degree Finder Verification Code"
        body = f"Your verification code is: {verification_code}"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send the email
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()

        st.write("Verification code sent successfully!")

    except Exception as e:
        st.error(f"Failed to send verification code: {e}")

    # Return the verification code for comparison
    return verification_code
