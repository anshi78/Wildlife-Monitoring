import os
import smtplib # You might need to add your full email logic here

# This is a placeholder. You will need to add your full email login details
# from .env variables (os.getenv) to make this work.
def send_email_alert(recipient_email, species, location, image_path):
    print(f"--- SIMULATING EMAIL ALERT ---")
    print(f"To: {recipient_email}")
    print(f"Subject: CRITICAL ALERT - {species.upper()} DETECTED!")
    print(f"Body: A {species} was detected at {location}.")
    print(f"Attachment: {image_path}")
    print(f"-------------------------------")
    
    # Example using smtplib (uncomment and configure to use)
    # SENDER_EMAIL = os.getenv("EMAIL_SENDER_ADDRESS")
    # SENDER_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")
    # SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    # SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    
    # try:
    #     message = f"Subject: CRITICAL ALERT - {species.upper()} DETECTED!\n\nA {species} was detected at {location}."
    #     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    #         server.starttls()
    #         server.login(SENDER_EMAIL, SENDER_PASSWORD)
    #         server.sendmail(SENDER_EMAIL, recipient_email, message)
    #     print("Successfully sent email alert.")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")