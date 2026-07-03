#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n")

import pymysql
import cgi
import cgitb
cgitb.enable()

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <style>
        body {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 400px;
            width: 100%;
        }
        h2 {
            color: #0d6efd;
        }
    </style>
</head>
<body>

<div class="login-box">
    <h2 class="text-center mb-4"><i class="fas fa-user-shield"></i> Admin Login</h2>
    <form method="post" action="/rajaproject/admin_login.py">
        <div class="mb-3">
            <label>Username</label>
            <input type="text" name="username" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Password</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
</div>

</body>
</html>
""")

form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")

if username and password:
    con = pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="studentdb"
    )
    cur = con.cursor()
    query = "SELECT * FROM Admin WHERE username=%s AND password=%s AND role='administrator'"
    cur.execute(query, (username, password))
    result = cur.fetchone()

    if result:
        print('<meta http-equiv="refresh" content="0;url=admin.py" />')
    else:
        print('<script>alert("Login Failed. Invalid Admin credentials!");</script>')

    cur.close()
    con.close()
