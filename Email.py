import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_verification_code(user_email):

    # Before sending the email, sanitize and check user_email
    user_email = user_email.strip()
    
    # Print email for debugging
    st.write(f"User email: {user_email}")
    
    # Ensure the email format is valid
    if "@" not in user_email or "." not in user_email:
        st.write("Invalid email address. Please try again.")
    else:
        # Create the email message
        msg['From'] = 'Social Network App <noreply.socialnetworkapp@gmail.com>'
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
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

    


