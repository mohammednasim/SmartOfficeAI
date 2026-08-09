from tools.email_tool import send_email

result = send_email(
    to_email="mohammednasimp@gmail.com",
    subject="Smart Office AI",
    message="Hello! This email was sent from Smart Office AI."
)

print(result)