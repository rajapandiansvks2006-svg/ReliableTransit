#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe

print("Content-Type: text/html\r\n\r\n")

import pymysql,cgi,cgitb
cgitb.enable()

con = pymysql.connect(
    host="localhost",
    port=3307,
    user="root",
    password="",
    database="studentdb"
)
cur = con.cursor()

f = cgi.FieldStorage()
uid = f.getvalue("id")

c = """SELECT * FROM login WHERE id = %s"""
cur.execute(c, (uid,))
r = cur.fetchall()

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        @media (min-width: 768px) {
            .navbar-toggler {
                display: none;
            }
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Dashboard</a>
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link text-light" href="#">Contact Us</a>
            </li>
        </ul>
    </div>
</nav>
<main class="container mt-4">
""")


for i in r:
    print(f"""
    <center><h2>Welcome {i[1]}</h2></center>""")
print("""
</main>
</body>
</html>
""")
