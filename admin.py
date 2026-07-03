#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\n")

import pymysql
import cgi
import cgitb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import html

cgitb.enable()
form = cgi.FieldStorage()

# Email setup
FROM_EMAIL = "rajapandiansvks2006@gmail.com"
APP_PASSWORD = "vqsymoxxwaxlbhpv"

def send_email(to_email, name, username, password):
    subject = "Ride Sharer Registration Approved"
    body = f"""Hello {name},

Your Ride Sharer registration has been approved.

Username: {username}
Password: {password}

You can now log in at:
http://localhost/rajaproject/ride_sharer_login.py

Thank you!"""

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

# Handle approval or rejection
if "action" in form and "user_id" in form and "role" in form:
    action = form.getvalue("action")
    user_id = form.getvalue("user_id")
    role = form.getvalue("role")

    con = pymysql.connect(host="localhost", port=3307, user="root", password="", database="studentdb")
    cur = con.cursor()

    if action == "accept":
        if role == "RideSeeker":
            cur.execute("UPDATE ride_seeker SET status='Accepted' WHERE id=%s", (user_id,))
        elif role == "RideSharer":
            username = form.getvalue("username")
            password = form.getvalue("password")
            cur.execute("UPDATE ride_sharer SET status='Accepted' WHERE id=%s", (user_id,))
            cur.execute("INSERT INTO login (username, password, role) VALUES (%s, %s, %s)",
                        (username, password, "RideSharer"))
            # Fetch email and name
            cur.execute("SELECT email, username FROM ride_sharer WHERE id=%s", (user_id,))
            email, name = cur.fetchone()
            send_email(email, name, username, password)
    elif action == "reject":
        if role == "RideSeeker":
            cur.execute("UPDATE ride_seeker SET status='Rejected' WHERE id=%s", (user_id,))
        elif role == "RideSharer":
            cur.execute("UPDATE ride_sharer SET status='Rejected' WHERE id=%s", (user_id,))

    con.commit()
    con.close()

# Fetch users
con = pymysql.connect(host="localhost", port=3307, user="root", password="", database="studentdb")
cur = con.cursor()

cur.execute("SELECT id, username, email, dob, address, role, status FROM ride_seeker")
seekers = cur.fetchall()

cur.execute("SELECT id, username, email, dob, address, role, status FROM ride_sharer")
sharers = cur.fetchall()
con.close()

# HTML Output
print("""
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f9fbe7; }
        .container { margin-top: 40px; }
        h2 { color: #2e7d32; }
        .btn-accept { background-color: #28a745; color: white; }
        .btn-reject { background-color: #dc3545; color: white; }
        input[type='text'], input[type='password'] {
            width: 100px; padding: 4px; margin-right: 6px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2 class="text-center mb-4">Admin Dashboard</h2>

    <h4>Ride Sharer Requests</h4>
    <table class="table table-bordered">
        <thead class="table-success">
            <tr>
                <th>ID</th><th>Username</th><th>Email</th><th>DOB</th><th>Address</th><th>Role</th><th>Status</th><th>Actions</th>
            </tr>
        </thead>
        <tbody>
""")

# Ride Sharer List
for u in sharers:
    uid, uname, email, dob, addr, role, status = u
    uname = uname or ""
    email = email or ""
    addr = addr or ""
    if status == "Pending":
        print(f"""
        <tr>
            <td>{uid}</td><td>{html.escape(uname)}</td><td>{html.escape(email)}</td>
            <td>{dob}</td><td>{html.escape(addr)}</td><td>{role}</td><td>{status}</td>
            <td>
                <form method="post" action="admin.py" style="display:inline-flex;">
                    <input type="hidden" name="action" value="accept">
                    <input type="hidden" name="role" value="RideSharer">
                    <input type="hidden" name="user_id" value="{uid}">
                    <input type="text" name="username" placeholder="Set Username" required>
                    <input type="password" name="password" placeholder="Set Password" required>
                    <button type="submit" class="btn btn-sm btn-accept">Accept</button>
                </form>
                <a href="?action=reject&user_id={uid}&role=RideSharer" class="btn btn-sm btn-reject">Reject</a>
            </td>
        </tr>
        """)
    else:
        print(f"""
        <tr>
            <td>{uid}</td><td>{html.escape(uname)}</td><td>{html.escape(email)}</td>
            <td>{dob}</td><td>{html.escape(addr)}</td><td>{role}</td><td>{status}</td>
            <td>-</td>
        </tr>
        """)

# Ride Seeker List
print("""
    </tbody></table>

    <h4>Ride Seeker Requests</h4>
    <table class="table table-bordered">
        <thead class="table-info">
            <tr>
                <th>ID</th><th>Username</th><th>Email</th><th>DOB</th><th>Address</th><th>Role</th><th>Status</th><th>Actions</th>
            </tr>
        </thead>
        <tbody>
""")

for u in seekers:
    uid, uname, email, dob, addr, role, status = u
    uname = uname or ""
    email = email or ""
    addr = addr or ""
    if status == "Pending":
        print(f"""
        <tr>
            <td>{uid}</td><td>{html.escape(uname)}</td><td>{html.escape(email)}</td>
            <td>{dob}</td><td>{html.escape(addr)}</td><td>{role}</td><td>{status}</td>
            <td>
                <a href="?action=accept&user_id={uid}&role=RideSeeker" class="btn btn-sm btn-accept">Accept</a>
                <a href="?action=reject&user_id={uid}&role=RideSeeker" class="btn btn-sm btn-reject">Reject</a>
            </td>
        </tr>
        """)
    else:
        print(f"""
        <tr>
            <td>{uid}</td><td>{html.escape(uname)}</td><td>{html.escape(email)}</td>
            <td>{dob}</td><td>{html.escape(addr)}</td><td>{role}</td><td>{status}</td>
            <td>-</td>
        </tr>
        """)

print("""
        </tbody>
    </table>
</div>
</body>
</html>
""")
