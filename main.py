#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
import os.path
print("content-type: text/html \r\n\r\n")
import pymysql,cgi,cgitb
cgitb.enable()
import pymysql

con = pymysql.connect(
    host="localhost",
    port=3307,              # ✅ FIXED: Must match running port
    user="root",
    password="",            # ✅ Use password if needed
    database="studentdb"    # ✅ Lowercase confirmed from your SHOW DATABASES;
)

cur=con.cursor()

print("""
<!DOCTYPE HTML>
<html>
<head>
</head>
<body>
<form method="post" enctype="multipart/form-data">
<input type="text" name="uname" placeholder="Enter name"><br><br>
<input type="text" name="dept" placeholder="Enter your department"><br><br>
<input type="file" name="pics" <br><br>
<input type="submit" name="sub" value="Register"><br><br>
</form>
</body>
</html>""")

f=cgi.FieldStorage()
if len(f) != None:
    submit = f.getvalue("sub")
    if submit != None:
        name = f.getvalue("uname")
        department = f.getvalue("dept")
        photo=f['pics']
        if photo.filename:
            fn=os.path.basename(photo.filename)
            open("dd/" + fn, "wb").write(photo.file.read())
            v = """insert into Students(Name,Department,photo) values('%s','%s','%s')""" % (name, department,fn)
            cur.execute(v)
            con.commit()
            print("""
            <script>
            alert("file Uploaded and data inserted!");
            </script>""")






