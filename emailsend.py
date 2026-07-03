#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\n")

import cgi
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

form = cgi.FieldStorage()
name = form.getvalue("name")
email = form.getvalue("email")
submit = form.getvalue("submit")

if submit:
    try:
        # ✅ Email config
        fromaddr = "your_gmail@gmail.com"
        password = "your_16_digit_app_password"  # <-- Paste your app password here
        toaddr = email

        subject = "Test Mail"
        body = f"Hello {name},\n\nThis is a test email sent from Python."

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(fromaddr, password)
        server.send_message(msg)
        server.quit()

        print("""
        <script>
        alert('Email sent successfully!');
        window.location.href = 'emailsend.py';
        </script>
        """)

    except Exception as e:
        print(f"<p style='color:red;'>Error occurred: {str(e)}</p>")

# ✅ Show the form (always visible)
print("""
<html>
    <body>
        <form method="post" action="emailsend.py">
            <label>Name: </label><input type="text" name="name"><br><br>
            <label>Email: </label><input type="email" name="email"><br><br>
            <input type="submit" name="submit" value="Send Email">
        </form>
    </body>
</html>
""")

