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
    <title>Login - ReliableTransit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- FontAwesome -->
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
            width: 100%;
            max-width: 400px;
        }
        .login-box h2 {
            color: #0d6efd;
        }
        .form-select {
            cursor: pointer;
        }
    </style>
</head>
<body>

<div class="login-box">
    <h2 class="text-center mb-4"><i class="fas fa-sign-in-alt"></i> Login</h2>

    <form action="/rajaproject/login.py" method="post">
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" placeholder="Enter username" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" placeholder="Enter password" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Role</label>
            <select name="role" class="form-select">
                <option value="administrator">Administrator</option>
                <option value="ride_sharer">Ride Sharer</option>
                <option value="ride_seeker">Ride Seeker</option>
            </select>
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <div class="text-center mt-3">
        <p>New user? <a href="register.html" class="text-decoration-none">Register here</a></p>
    </div>
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")
role = form.getvalue("role")

con = pymysql.connect(
    host="localhost",
    port=3307,
    user="root",
    password="",
    database="studentdb"
)
cur = con.cursor()
query = "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s"
cur.execute(query, (username, password, role))
result = cur.fetchone()

if result:
    if role == "administrator":
        print('<meta http-equiv="refresh" content="0;url=admin.html" />')
    elif role == "ride_sharer":
        print('<meta http-equiv="refresh" content="0;url=ride-sharer.html" />')
    elif role == "ride_seeker":
        print('<meta http-equiv="refresh" content="0;url=ride-seeker.html" />')
else:
    print("""<script>
    alert("Login Failed. Invalid credentials!");
    </script>""")


cur.close()
con.close()
