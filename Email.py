import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_verification_code(user_email):
    
    
    sender_email = "noreply.socialnetworkapp@gmail.com"
    sender_password = "mmfg chsp hbhz hhav"  # It's highly recommended to store this securely, not in the code
    
    user_email = st.text_input("Enter your email address:")
    
    # Generate a random 4-digit verification code
    verification_code = random.randint(1000, 9999)
    
    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start a secure TLS connection
        server.login(sender_email, sender_password)
    
        st.write("SMTP Server Connected and Logged In Successfully.")
    except Exception as e:
        st.write(f"Failed to connect to the SMTP server or login: {str(e)}")
    
    # Create the email message
    subject = "Your Verification Code"
    body = f"Your verification code is: {verification_code}"
    msg = MIMEMultipart()
    msg['From'] = 'Social Network App <noreply.socialnetworkapp@gmail.com>'
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Check and print out email content for debugging
    st.write("\n--- Email Content ---")
    st.write(f"Subject: {subject}")
    st.write(f"Body: {body}")
    st.write(f"To: {user_email}")
    
    # Send the email
    try:
        server.sendmail(sender_email, user_email, msg.as_string())
        st.write("\nEmail sent successfully!")
    except smtplib.SMTPRecipientsRefused as e:
        st.write(f"\nFailed to send email. Recipient refused: {e.recipients}")
    except smtplib.SMTPSenderRefused as e:
        st.write(f"\nFailed to send email. Sender refused: {e.sender}")
    except smtplib.SMTPDataError as e:
        st.write(f"\nFailed to send email. Data error: {e}")
    except smtplib.SMTPException as e:
        st.write(f"\nSMTP Error: {str(e)}")
    
    # Quit the server after sending the email
    server.quit()
    return verification_code


