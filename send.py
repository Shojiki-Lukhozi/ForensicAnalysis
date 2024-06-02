import smtplib
import random
import time  # Import the time module

# Mailtrap SMTP server configuration
print("One!")
smtp_server = "sandbox.smtp.mailtrap.io"
smtp_port = 2525
username = ""
password = ""

# Fake email addresses
senders = [
    "John Doe <john@example.com>",
    "Jane Smith <jane@example.com>",
    "Drug Lord <boss@darkweb.com>",
    "Alice Johnson <alice@example.com>",
    "Bob Brown <bob@example.com>"
]
receivers = [
    "Test User <test@example.com>",
    "Agent Smith <agent@cia.gov>",
    "Dark Net Buyer <buyer@darkweb.com>",
    "Charlie Davis <charlie@example.com>",
    "Daisy White <daisy@example.com>"
]

# Subject lines for different types of emails
subjects_illegal = [
    "Re: Shipment of special herbs",
    "Confidential: The package",
    "Follow-up: Your order",
    "Re: The merchandise",
    "Regarding the product"
]
subjects_neutral = [
    "Meeting Schedule",
    "Project Update",
    "Lunch Invitation",
    "Weekly Report",
    "Greetings"
]

# Email bodies for different types of emails
bodies_illegal = [
    "The shipment of 'special herbs' has arrived. The 'books' are ready for pickup.",
    "We've received the 'candy'. It's high quality. Let me know where to deliver.",
    "Your order of 'party supplies' is confirmed. Please make the payment through the usual method.",
    "The 'merchandise' is ready. Do you want it delivered to the usual spot?",
    "The product is as discussed. Contact me for further details."
]
bodies_neutral = [
    "Looking forward to our meeting next week. Please confirm your availability.",
    "Here's the update on the project status. All milestones are on track.",
    "Let's have lunch at the new place downtown tomorrow. Are you available?",
    "Attached is the weekly report. Please review and provide your feedback.",
    "Hope you are doing well. Just wanted to say hi and catch up."
]

delay_between_emails = 2  # Adjust this as needed

def create_email(sender, receiver, subject, body):
    return f"Subject: {subject}\nTo: {receiver}\nFrom: {sender}\n\n{body}"

print("Three!")

def send_email(server, sender, receiver, message):
    server.sendmail(sender, receiver, message)

# Connect to the SMTP server and send emails
try:
    # Connect to the SMTP server and send emails
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        
        for i in range(30):
            if i > 0:
                print(f"Waiting for {delay_between_emails} seconds before sending the next email.")
                time.sleep(delay_between_emails)  # Add delay between emails
            
            # Randomly choose whether the email is illegal or neutral
            if random.choice([True, False]):
                subject = random.choice(subjects_illegal)
                body = random.choice(bodies_illegal)
            else:
                subject = random.choice(subjects_neutral)
                body = random.choice(bodies_neutral)
            
            sender = random.choice(senders)
            receiver = random.choice(receivers)
            
            email_message = create_email(sender, receiver, subject, body)
            try:
                send_email(server, sender, receiver, email_message)
                print(f"Sent email {i+1}/30")
            except Exception as e:
                print(f"Failed to send email {i+1}/30: {e}")

    print("All emails sent successfully.")
except Exception as e:
    print(f"Failed to connect or send emails: {e}")
