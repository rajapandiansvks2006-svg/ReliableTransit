#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\r\n\r\n")

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
cur.execute("SELECT * FROM Students")
rows = cur.fetchall()

print("""
<!DOCTYPE html>
<html>
<head>
    <title>Student Cards</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
    <div class="row">
""")

for i in rows:
    name = i[1]
    photo = i[4]

    print(f"""
        <div class="col-md-4 mb-4">
            <div class="card">
                <img src="./images/{i[4]}" class="card-img-top" alt="{name}" height="200">
                <div class="card-body">
                    <h5 class="card-title">{name}</h5>
                </div>
            </div>
        </div>
    """)

print("""
    </div>
</div>
</body>
</html>
""")
